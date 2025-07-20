from langchain_google_vertexai import VertexAIImageGeneratorChat, ChatVertexAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from django.conf import settings
from typing import List, Dict
from .storage import image_storage_url
import base64
import os 




class SocialMediaGenerator:
    def __init__(self):
        # project = GOOGLE_CLOUD_PROJECT
        # location = GOOGLE_PROJECT_LOCATION
        project = settings.GOOGLE_CLOUD_PROJECT
        location = settings.GOOGLE_PROJECT_LOCATION

        # Text LLM and Image generators (Vertex AI)
        self.llm = ChatVertexAI(
            model_name="gemini-2.0-flash-exp",
            temperature=0.7,
            max_output_tokens=1500,
            project=project,
            location=location
        )

        self.img_llm = VertexAIImageGeneratorChat(
            model_name="imagen-4.0-generate-preview-06-06",
            project=project,
            location=location
        )

        self.output_parser = StrOutputParser()
    
    def create_platform_specific_prompt(self, platform:str):
        platform_specs = {
            "twitter": {
                "limit": "280 characters",
                "style": "concise, witty, engaging; relevant hashtags",
                "features": "Use 1-3 hashtags; consider trending topics",
                "img_aspect": "16:9"
            },
            "linkedin": {
                "limit": "1300 characters",
                "style": "professional, informative",
                "features": "Industry insight, pro hashtags",
                "img_aspect": "1.91:1"
            },
            "instagram": {
                "limit": "500 characters",
                "style": "visually descriptive, lifestyle",
                "features": "5-10 hashtags, suggest visuals",
                "img_aspect": "1:1"
            },
            "facebook": {
                "limit": "500 characters",
                "style": "conversational, community-focused",
                "features": "Ask questions/calls-to-action",
                "img_aspect": "1.91:1"
            }
        }

        spec = platform_specs.get(platform.lower(), platform_specs['twitter'])
        system_message = f"""You are a social media content creator for {platform.upper()}.
            Guidelines:
            - Limit: {spec['limit']}
            - Style: {spec['style']}
            - Features: {spec['features']}
            Create engaging, original posts to maximize platform performance.
        """

        prompt = ChatPromptTemplate.from_messages([
            ("system", system_message),
            ("human", """Create a {platform} post about: {topic}
            Context: {context}
            Tone: {tone}
            Target audience: {audience}
            Only generate the post content.""")
        ])

        return prompt, spec["img_aspect"]

    def generate_post(self, 
            topic: str, 
            platform: str = "twitter", 
            context: str = "", 
            tone: str = "professional", 
            audience: str = "general" ) -> str:
        prompt, _ = self.create_platform_specific_prompt(platform)
        chain = prompt | self.llm | self.output_parser

        result = chain.invoke(
            {
            "topic": topic,
            "platform": platform,
            "context": context,
            "tone": tone,
            "audience": audience
            }
        )
        return result
    # generate image prompt
    def generate_image_prompt(self,
                        user_desc: str, 
                        platform: str, 
                        brand_handle, brand_colors,
                        context: str = "") -> str:

        _, aspect = self.create_platform_specific_prompt(platform)
        platform_styles = {
            "twitter": "vibrant, eye-catching, modern, minimal text",
            "linkedin": "professional, clean, innovative, no text",
            "instagram": "aesthetic, bold, visually stunning, no text",
            "facebook": "shareable, inclusive, visually engaging, minimal text"
        }
        style = platform_styles.get(platform.lower(), platform_styles['twitter'])
        # Construct the main (positive) prompt
        main_prompt = f"""
            Generate a visually compelling image for a {platform} post:
            Instructions:
             - Main concept: {user_desc}
             - Style: {style}. Aspect ratio: {aspect}.
             - Context: {context}.
            Design Guidelines:
            
            - Place the handle (@{brand_handle}) subtly in one corner as a small watermark or badge.
            - Do not include any other text, hashtags, post content, or context information on the image.
            - Do not write color codes, numbers, or color names anywhere on the image
            - Focus on aesthetics, platform suitability, and clean visual storytelling.
            """

        return main_prompt



    # generate image 
    def generate_image(self, 
                topic: str, 
                brand_handle, 
                brand_colors,
                platform: str = "twitter", 
                context: str = "", ) -> dict:
        try:
            prompt = self.generate_image_prompt(topic, platform,  brand_handle, brand_colors, context,)
            # print(prompt)
            # messsage = [HumanMessage(content=[prompt])]
            image_result = self.img_llm.invoke(prompt)
            return image_result
        except Exception as e:
            print(f"Image generation failed: {e}")
            return None


    # generate post with image
    def generate_post_with_image(self, topic: str, platform: str = "twitter",
                                 context: str = "", tone: str = "professional",
                                 brand_handle:str= None, brand_colors:list = None,
                                 audience: str = "general") -> Dict[str, str]:
        
        # Generate text post and image
        post = self.generate_post(topic, platform, context, tone, audience)
        image_data = self.generate_image(topic,  brand_handle, brand_colors, platform, context,)
        image_url = image_data.content[0]["image_url"]["url"].split(",")[-1] if image_data else None
        url = image_storage_url(base64.b64decode(image_url))
        return {"platform": platform, "post": post, "image_url": url}
    
    # generate multiple image with post
    def generate_multiple_posts_with_images(self,
                                    topic: str,
                                    platforms: List[str] = ["twitter", "linkedin", "instagram"],
                                    context: str = "",
                                    tone: str = "professional",
                                    brand_handle: str=None, 
                                    brand_colors: list=None,
                                    audience: str = "general") -> Dict[str, Dict]:
        results = []
        for platform in platforms:
            result = self.generate_post_with_image(
                topic=topic,
                platform=platform,
                context=context,
                tone=tone,
                audience=audience,
                brand_handle=brand_handle, 
                brand_colors=brand_colors,
            )
            results.append(result)

        return {"topic": topic, "contents": results}
    
    # generate psot variants 
    def generate_post_variants( 
                self, topic: str, platform: str = "twitter", count: int = 3,
                              context: str = "", tone: str = "professional",
                              audience: str = "general") -> List[Dict]:

        variants = []
        for i in range(count):
            variant_context = f"""
                {context} (Variant {i+1} Make this version 
                {"more engaging" if i == 0 else  
                "more informative" if i==1 else "more creative"} )
            """
            post = self.generate_post(topic, platform, variant_context, tone, audience)
            image_data = self.generate_image(topic, platform, variant_context)
            image_url = image_data.content[0]["image_url"]["url"].split(",")[-1] if image_data else None
            url = image_storage_url(base64.b64decode(image_url))
            variants.append({"post": post, "image_url": url})
        return variants


#####################################################################################################33333333
# result = SocialMediaGenerator()
# data = result.generate_post_with_image(topic="agentic in ai")
# print(data)
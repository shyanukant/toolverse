from langchain_google_vertexai import VertexAIImageGeneratorChat, ChatVertexAI
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
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
                
            },
            "linkedin": {
                "limit": "1300 characters",
                "style": "professional, informative",
                "features": "Industry insight, pro hashtags",
                
            },
            "instagram": {
                "limit": "500 characters",
                "style": "visually descriptive, lifestyle",
                "features": "5-10 hashtags, suggest visuals",
                
            },
            "facebook": {
                "limit": "500 characters",
                "style": "conversational, community-focused",
                "features": "Ask questions/calls-to-action",
                
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

        return prompt

    def generate_post(self, 
            topic: str, 
            platform: str = "twitter", 
            context: str = "", 
            tone: str = "professional", 
            audience: str = "general" ) -> str:
        prompt = self.create_platform_specific_prompt(platform)
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
    def generate_image_prompt(self) -> str:

        # _, aspect = self.create_platform_specific_prompt(platform)
      
        # Construct the main (positive) prompt
        main_prompt = """
            Transform this short description into a detailed prompt for image generation:
            Instructions:
             - Style: modern, versatile, visually compelling, suitable for all social media platforms
             - Main concept: {user_desc}
             - Tone: {tone}.
             - Context: {context}.
            Design Guidelines:
            
            - Place the handle (@{brand_handle}) subtly in one corner as a small watermark or badge.
            - Prompt should be start with overall goal, Visual Style, Design Guidelines , don't give extra and introduction , only response a prompt for image.
            - Make sure NOT to mention color codes or hashtags.
            - Focus on aesthetics, platform suitability, and clean visual storytelling.
            """
        prompt_template = PromptTemplate.from_template(main_prompt) 
        return prompt_template



    # generate image 
    def generate_image(self, 
                topic: str, 
                tone: str,
                brand_handle, 
                brand_colors,
                platform: str = "twitter", 
                context: str = "", ) -> dict:
        try:
            # Chain 1
            prompt_template = self.generate_image_prompt()
            prompt_text = prompt_template.format(
                user_desc=topic,
                tone=tone,
                brand_handle=brand_handle,
                context=context
            )

            detailed_prompt = self.llm.invoke(prompt_text)
            if hasattr(detailed_prompt, "content"):
                prompt_text = detailed_prompt.content
            else:
                prompt_text = str(detailed_prompt)
            print(prompt_text)
            # chain 2
            image_result = self.img_llm.invoke(prompt_text)
            # print(prompt)
            return image_result
        except Exception as e:
            print(f"Image generation failed: {e}")
            return None

    
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
            post = self.generate_post(
                topic=topic, 
                platform=platform, 
                context=context, 
                tone=tone, 
                audience=audience)
            result = {"platform": platform, "post": post}
            results.append(result)
           
        image_data = self.generate_image(topic, tone, brand_handle, brand_colors, platform, context,)
        image_url = image_data.content[0]["image_url"]["url"].split(",")[-1] if image_data else None
        url = image_storage_url(base64.b64decode(image_url))

        return {"topic": topic, "contents": results, "img_url": url}
    
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
# # data = result.generate_image(topic="agentic in ai" , tone="educational", brand_colors=None, brand_handle="shyanu")
# data = result.generate_multiple_posts_with_images(
#                                     topic="agentic in ai",
#                                     platforms = ["twitter"],
#                                     tone= "educational",
#                                     brand_handle="shyanu"
#                                     )
# print(data)
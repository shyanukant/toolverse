from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage
from typing import Dict, List, Optional
from django.conf import settings
import json




class SocialMediaGenerator:
    def __init__(self):
        
        # initialize with google gemini model 
        self.llm = ChatGoogleGenerativeAI(
            model = "gemini-2.0-flash-exp",
            temperature = 0.7,
            max_output_token = 1500,
            google_api_key = API_KEY if API_KEY else settings.GOOGLE_GEMINI_API_KEY

        )
        self.output_parser = StrOutputParser()

    def create_platform_specific_prompt(self, platform:str):
        """Create platform-specific prompt templates."""
        platform_specs = {
            "twitter": {
                "limit": "280 characters",
                "style": "concise, witty, and engaging with relevant hashtags",
                "features": "Use 1-3 relevant hashtags and consider trending topics"
            },
            "linkedin": {
                "limit": "1300 characters for optimal engagement",
                "style": "professional, informative, and thought-provoking",
                "features": "Include industry insights and professional hashtags"
            },
            "instagram": {
                "limit": "500 characters",
                "style": "visually descriptive, engaging, and lifestyle-focused",
                "features": "Use 5-10 relevant hashtags and suggest visual elements"
            },
            "facebook": {
                "limit": "500 characters for optimal engagement",
                "style": "conversational, community-focused, and engaging",
                "features": "Encourage interaction with questions or calls-to-action"
            }
        }

        spec = platform_specs.get(platform.lower(), platform_specs['twitter'])

        # system message template 
        system_message = f"""You are a social media content creator specializing in {platform.upper()} posts. 
        
        Platform Guidelines:
        - Character limit: {spec['limit']}
        - Style: {spec['style']}
        - Special features: {spec['features']}
        
        Create engaging, original content that follows {platform} best practices.
        Make sure the content is appropriate for the platform's audience and culture.
        """

        # setup prompt template
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system_message),
                ("human", """
                    Create a {platform} post about: {topic}
                
                    Additional context: {context}
                    Tone: {tone}
                    Target audience: {audience}
                    
                    Generate only the post content, ready to publish.
                """)
                ]
        )

        return prompt

    # post generation funtions
    def generate_post(self,
                    topic: str, 
                    platform: str = "twitter",
                    context: str = "",
                    tone: str = "professional",
                    audience: str = "general" 
                    ) -> str:
                    
        """
            Generate a social media post for the specified platform.
            
            Args:
                topic: The main topic/subject of the post
                platform: Target platform (twitter, linkedin, instagram, facebook)
                context: Additional context or details
                tone: Tone of the post (professional, casual, humorous, etc.)
                audience: Target audience description
                
            Returns:
                Generated social media post content 
        """

        # Create prompt 
        prompt = self.create_platform_specific_prompt(platform)

        # Create chain ==== prompt → model → parser ==== 
        # it's overloaded operator usage ==> connect prompt output as llm input and then output parser input ( combine ) 
        chain = prompt | self.llm | self.output_parser  

        # generate the post

        result = chain.invoke(
            {
                "topic": topic,
                "platform": platform,
                "context": context,
                "tone": tone,
                "audience": audience
            }
        )

        return result.strip()


    # multiple post generation function
    def generate_multiple_posts(
                            self,
                            topic: str,
                            platforms: List[str] = ["twitter", "linkedin", "instagram"],
                            context: str = "",
                            tone: str = "professional",
                            audience: str = "general") -> Dict[str, str]:

        """
            Generate posts for multiple platforms simultaneously.
            
            Returns:
                Dictionary with platform names as keys and generated posts as values
        """
        posts = {}

        for platform in platforms:
            try:
                post = self.generate_post(
                    topic=topic,
                    platform=platform,
                    context=context,
                    tone=tone,
                    audience=audience
                )
                posts[platform] = post

            except Exception as e:
                print(e)
                posts[platform] = "Error generating post: {str(e)}"
        return posts


    def generate_post_variants(
        self,
        topic: str,
        platform: str = "twitter",
        count: int = 3,
        context: str = "",
        tone: str = "professional",
        audience: str = "general") -> List[str]:

        """
            Generate multiple variants of a post for A/B testing.
            
            Returns:
                List of post variants
        """
        variants = []
        for i in range(count):
            # Modify the prompt slightly for each variant
            variant_context = f"{context} ( Variant {i+1}: Make this version {'More engaging' if i==0 else 'More informative' if i==1 else 'more creative' })"
            try:
                variant = self.generate_post(
                    topic=topic,
                    platform=platform,
                    context=variant_context,
                    tone=tone,
                    audience=audience
                )
                variants.append(variant)
            except Exception as e:
                print(e)
                variants.append(f"Error generating variant {i+1}: {str(e)}")
        return variants


content = SocialMediaGenerator()

print(content.generate_post_variants("email marketing"))


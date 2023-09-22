import os
from re import sub
from json import loads
from .response_parser import parser
from langchain.llms import OpenAI
from langchain.chains import LLMChain
from langchain.chains import SequentialChain
from langchain.prompts import PromptTemplate, ChatPromptTemplate

OPENAI_KEY = os.environ.get('OPENAI_API_KEY')
# templae string 

template_stirng = """You are the dedicated content creator and skilled social media marketer for our company. In this dynamic role, 
            your responsibility encompasses crafting top-notch content within the realm of "{topic}" while maintaining an ingenious, professional, and captivating tone. 
            Your role includes creating a compelling content strategy, engaging with our audience, leveraging trends, analyzing insights, and staying at the forefront of industry trends to ensure our brand's online presence flourishes. Your content will not only resonate deeply with our target audience but also drive impactful results across diverse platforms.

            So create content on this topic "{topic}" with a "{tone}" tone and your goal is "Create compelling and shareable content that resonates with the audience, encourages interaction."

                """


template_stirng2 = """You are the primary content creator for our organization, 
                responsible for crafting engaging content for social media platforms and optimizing it for SEO. 
                Your goal is to create content that resonates with the audience and enhances our brand's online presence. 
            
            Your expertise in content creation will play a pivotal role in enhancing our brand's online presence and engagement across these diverse platforms.

           For SEO purposes, generate the following SEO information as key, value pair.

            Now, for the given content "{contents}" with a "{tone}" tone, create content for the following social media platforms: {platforms}.

            {format_instructions}

            """
# main functon of llm model
def llm(topic, tone, platforms):

    llm = OpenAI(temperature=.7, openai_api_key=OPENAI_KEY, max_tokens=750)
    
    prompt_template = PromptTemplate(input_variables=["topic", "tone"], template=template_stirng, validate_template=True)
    chain1 = LLMChain(llm=llm, prompt=prompt_template, output_key="contents")

    output_parser = parser()
    format_instructions = output_parser.get_format_instructions()

    prompt_template2 = PromptTemplate(
        template= template_stirng2,
        input_variables=['contents', 'tone', 'platforms'],
        partial_variables={'format_instructions': format_instructions},
        output_parser=output_parser
    )
    # prompt = ChatPromptTemplate.from_template(template_stirng)
    # messages = prompt.format_messages(topic=topic, tone=tone, platforms=platforms, format_instructions=format_instructions)
    # output = llm(messages)

    chain2 = LLMChain(llm=llm, prompt=prompt_template2, verbose=True)

    # This is the overall chain where we run these two chains in sequence.
    overall_chain = SequentialChain(
        chains=[ chain1, chain2],
        input_variables=["topic", "tone", "platforms"],
        # Here we return multiple variables
        output_variables=["text"],
        verbose=True)

    response = overall_chain({"topic":topic, "tone": tone,  "platforms": platforms })

    # clean response
    output = response['text'].split(':', 1)[1]
    clean_output = sub(r'[\x00-\x1F\x7F-\x9F]', '', output)
    return loads(clean_output)

# print(llm('self-taught programmer', 'educational', ['facebook', 'instagram', 'linkedin']))

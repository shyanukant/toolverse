from django import forms
from brands.models import BrandModel
from django.contrib.auth.models import User

# prompt user input forms#
PLATFORMS_CHOICES = [
    ("facebook", "Facebook"),
    ("instagram", "Instagram"),
    ("twitter", "Twitter"),
    ("linkedin", "LinkedIn"),
    # ("youtube", "YouTube"),
    # ("pinterest", "Pinterest"),
]

TONES_CHOICES = [
        ( "Providing clear and factual information in a straightforward manner.", "Informative"),
            ( "Sharing insights tips and knowledge to educate theaudience.", "Educational"),
            ( "Writing in a relaxed and conversational style as if chatting with a friend.", "Casual"),
            ( "Infusing humor and wit to entertain and engage theaudience.", "Humorous"),
            ( "Motivating and uplifting theaudience with positive messages.", "Inspiring"),
            ( "Maintaining a formal and polished tone suitable for industry-related content.", "Professional"),
            ( "Asking questions and sharing content that stimulates deep thinking and discussion.", "Thought-Provoking"),
            ( "Showing understanding and empathy towards theaudience's challenges and concerns.", "Empathetic"),
            ( "Encouraging dialogue and interaction by posing questions and seeking opinions.", "Conversational"),
            ( "Communicating with authenticity and genuine emotions.", "Sincere"),
            ( "Using sarcasm to create a light-hearted and relatable tone.", "Sarcastic"),
            ( "Sparking curiosity by raising questions and inviting curiosity.", "Inquisitive"),
            ( "Sharing stories and quotes to motivate and uplift theaudience.", "Inspirational"),
            ( "Sharing personal anecdotes and experiences to create a sense of connection.", "Personal"),
            ( "Creating a sense of urgency to encourage immediate action.", "Urgent"),
            ( "Using powerful language to inspire action and change.", "Motivational"),
            ( "Incorporating playful language and elements to add fun and excitement.", "Playful"),
            ( "Presenting yourself as an expert with a confident and knowledgeable tone.", "Authoritative"),
            ( "Evoking feelings of nostalgia by referencing the past and cherished memories.", "Nostalgic"),
            ( "Expressing curiosity and enthusiasm to learn and explore together with theaudience.", "Curious"),
]

char_class = 'block p-2.5 w-full text-sm text-gray-900 bg-gray-50 rounded-lg border border-gray-300 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-600 dark:border-gray-500 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500'
choice_class = 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-primary-500 focus:border-primary-500 block w-full p-2.5 dark:bg-gray-600 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500'

class PromptForm(forms.Form):
    subject = forms.CharField(
        required=True,
        label="Enter the topic/subject",
        widget=forms.TextInput(
            attrs={
                "placeholder": "your topic...",
                "class": char_class
            }
        )
    )
    prompt = forms.CharField(
        label="Enter Your Prompt",
        widget=forms.Textarea(
            attrs={
                'placeholder': 'Prompt...',
                'class':char_class
                   }),  # Use 'placeholder' with lowercase 'p'
        required=True
    )
    
    platforms = forms.MultipleChoiceField(
        label="Platforms",
        widget=forms.CheckboxSelectMultiple(),
        choices= PLATFORMS_CHOICES,
        required=True
    )

    tone = forms.ChoiceField(
        label="tone",
        choices=TONES_CHOICES,
        widget=forms.Select(
            attrs={'class': choice_class}),
        required=True
    )

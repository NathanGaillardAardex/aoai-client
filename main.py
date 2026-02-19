import os

from pydantic import BaseModel
from dotenv import load_dotenv

from oai_client import OpenAIClient

load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")
if not API_KEY:
    raise RuntimeError("Missing OPENAI_API_KEY in .env")

def untyped_example():
    client = OpenAIClient(
        open_ai_key=API_KEY,
        endpoint="https://api.openai.com/v1",
        model="gpt-5-nano-2025-08-07",
        system_role="You are a helpful assistant that writes bedtime stories for children.",
    )
    
    response = client.request("Write a one-sentence bedtime story about a unicorn.")
    print(response)

def typed_example():
    class Summary(BaseModel):
        title: str
        key_points: list[str]
    
    
    client = OpenAIClient(
        open_ai_key=API_KEY,
        endpoint="https://api.openai.com/v1",
        model="gpt-5-nano-2025-08-07",
        system_role="You list the key points of a text. You come up with a title that suits the text.",
        response_format=Summary,
    )
    
    result = client.request("""
    Online friendships – true or false? 
    In recent years, technology has taken over our daily lives. Many
    people claim that they simply couldn’t imagine a life without the
    internet and social media. So are your online friendships doing you
    more harm than good?
    It has become commonplace in our society to argue that
    technology is the reason for people being socially distant and
    experiencing loneliness. Some studies do show a correlation
    between social media usage and low self-esteem, although there is
    no solid proof showing that this is the main cause. Indeed, others
    have come to the defence of the internet and claim it has done the
    opposite – helped to revive social relationships. Some people find it
    easier to form relationships when they are hidden behind a screen.
    It allows them to be themselves without fear of rejection, ridicule
    and judgement. Soon, they become confident enough to merge
    their virtual personalities with their offline personalities, becoming
    a more authentic version of themselves.
    However, it can be said that online relationships are weaker and
    not as real as face-to-face relationships. Online relationships are
    formed easily and quickly. They’re not the same as a physical
    relationship. You might not know anything about an online friend
    other than the things they choose to post on the internet. Unless
    you make a point of communicating with all of them for at least
    two hours every week, you can’t even call it a real friendship. The
    strength of an offline relationship lies in the experiences you share
    together in the real world.
    True, it could be argued that online relationships are not
    particularly meaningful, but saying that social media friendships
    are false is not correct. ‘You and your real friends may not
    always be able to meet in person,’ explains one lifestyle expert.
    Social media can be used to keep in touch and ensure that your
    The learner uses a heading that
    is relevant to the topic of the article.
    The learner introduces the topic in
    the first paragraph and uses a
    rhetorical question to engage the
    reader.
    The paragraph identifies
    contrasting viewpoints, making it clear
    where there is support for one view or
    another.
    The learner is trying to vary
    sentence structure and vocabulary.
    The learner uses an appropriate
    linking word at the beginning of the
    paragraph to show they are about to
    offer a new contrasting argument.
    The learner develops the
    argument that online friendships are
    2
    Comments
    relationship stays in tact until the next time you meet, and where
    else can you bond over silly and fun things like memes and cute
    cat videos? Your social media friendship ensures that no matter
    how far apart you are, you can always be there for each other.
    """)
    print(result)


if __name__ == '__main__':
    untyped_example()
    typed_example()
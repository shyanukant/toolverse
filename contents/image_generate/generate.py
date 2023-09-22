import requests
from random import randint
from django.conf import settings
from .text_wraper import wrap_text
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageFilter

MEDIA_ROOT = settings.MEDIA_ROOT
def generate(heading, body, website_link, image_path, logo_path, font_style,heading_font_size, body_font_size, link_font_size,  width, height, logo_size, margin , color_white, color_black, color_blue, background_color):
    padding = 10
    post_image = Image.new("RGB", (width, height), background_color)
    # Open or create an image object
    
    img = Image.open(requests.get(image_path, stream=True).raw)
    img = img.filter(ImageFilter.GaussianBlur(radius=15))
    # Create an ImageDraw object
    img = img.resize((width, height), Image.LANCZOS)
    # # Convert the image to RGBA mode
    draw = ImageDraw.Draw(img)
    
    font_heading = ImageFont.truetype(font_style, heading_font_size)
    font_body = ImageFont.truetype(font_style, body_font_size)
    font_link = ImageFont.truetype(font_style, link_font_size)
    
    # Get the maximum width for the text
    text_width = width - 2 * margin
    
    lines = wrap_text(heading, font_heading, text_width)
    
    heading_y = margin
    # loop line
    for line in lines:
        # Draw heading on top of image
        heading_left, heading_upper, heading_right, heading_lower = font_heading.getbbox(line)
        heading_width = heading_right - heading_left
        heading_height = heading_lower - heading_upper
        
        heading_x = (width - heading_width) / 2
        draw.text((heading_x, heading_y), line, font=font_heading, fill=color_white)
        
        heading_y += heading_height + padding
    
    # Draw body in middle of image
    body_lines = wrap_text(body, font_body, text_width)
    body_y = (height/2) - margin
    for body_line in body_lines:
        
        body_left, body_upper, body_right, body_lower = font_body.getbbox(body_line)
        body_width = body_right - body_left
        body_height = body_lower - body_upper

        body_x = (width - body_width) / 2
        draw.text((body_x, body_y), body_line ,align='center',      font=font_body, fill=color_black)
        body_y += body_height
    
    
    
    # Draw website link in button
    #link
    link_left, link_upper, link_right, link_lower = font_link.getbbox(website_link)
    link_width = link_right - link_left
    link_height = link_lower - link_upper
    
    # button
    button_width = link_width + 20
    button_height = link_height + 10
    button_x = (width - button_width) / 2
    button_y = height - button_height - margin
    draw.rounded_rectangle((button_x, button_y, button_x + button_width, button_y + button_height),radius=4 ,  fill=color_blue)
    
    link_x = (width - link_width) / 2
    link_y = button_y + (button_height - link_height) / 2
    draw.text((link_x, link_y), website_link, font=font_link, fill=color_white)
    
    # Paste logo on top right corner
    logo_image = Image.open(logo_path)
    
    # Convert the image to RGBA mode
    logo_image = ImageOps.fit(logo_image, logo_size)
    logo_x = width - logo_size[0] - 20
    logo_y = 20
    img.paste(logo_image, (logo_x, logo_y))
    img_num = randint(1, 100)
    # Save the image with template
    img.save(MEDIA_ROOT/f"{str(img_num)}image_template.jpg")

    return f"{str(img_num)}image_template.jpg"

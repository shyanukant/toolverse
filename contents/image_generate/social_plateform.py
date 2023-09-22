import generate
# Define the dimensions of the Facebook post (in pixels)
# width = 800  # Width of the post
# height = 630  # Height of the post

# pinterest
margin = 80
width = 1000
height = 1500
heading_font_size = 72
body_font_size = 48
link_font_size = 36


# instagram
margin = 80
width = 1080
height = 1080
heading_font_size = 72
body_font_size = 48
link_font_size = 36

# facebook
margin = 60
width = 1200
height = 630
heading_font_size = 72
body_font_size = 48
link_font_size = 36

# Define color
color_white = (255, 255, 255)
color_black = (220, 133, 220)
color_blue = (0, 0, 255)

background_color = (255, 255, 255)
logo_size = (100, 100)
logo_path = "logo.png"
image_path = "graudmire.png"
# Define text content
heading = "Welcome to My Website"
body = "This is a sample website that I created using Python and Pillow. I hope you like it."
website_link = "www.mywebsite.com"

# Define font
font_style = "C:/Windows/Fonts/POORICH.TTF"

print(generate.generate(heading, body, website_link, image_path, logo_path, font_style,heading_font_size, body_font_size, link_font_size,  width, height, logo_size, margin , color_white, color_black, color_blue, background_color))
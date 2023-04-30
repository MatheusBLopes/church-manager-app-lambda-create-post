from PIL import Image, ImageDraw, ImageFont
import os

class ThumbnailAndPostCreator:
    def __init__(self, day_of_the_week, date, preacher, theme):
        self.day_of_the_week = day_of_the_week
        self.date = date
        self.preacher = preacher
        self.theme = theme

        self.colors_palette = {
            "DOMINGO": "#00C2CB",
            "QUARTA": "#FF1700",
            "SÁBADO": "#F1D900"
        }


        self.color_to_use = self.colors_palette.get(self.day_of_the_week)
        self.background_image = Image.open(os.path.abspath("app/src/bg.png"))

        self.montserrat_arabic_font = os.path.abspath('app/src/fonts/montserrat-arabic-500.otf')
        self.libre_baskerville_font = os.path.abspath('app/src/fonts/libre-baskerville-regular.ttf')
        self.montserrat_medium_font = os.path.abspath('app/src/fonts/montserrat-medium-500.ttf')

        self.draw = None
        self.image = None

        

    def draw_centered_white_text(self, text, font_size, height, font):
        # Choose font
        font = ImageFont.truetype(font, font_size)
        
        # Get size of text
        text_width, text_height = self.draw.textbbox((0, 0), text, font=font)[2:]
        
        # Calculate position for text to be centered vertically
        x = (self.image.width - text_width) // 2
        y = (font_size * 2 - text_height) // 2
        
        # Draw text
        self.draw.text((x, y + height), text, font=font, fill='white')
    

    def draw_text_under_gradient(self):
        width, height = self.image.size
        txt_layer = Image.new("RGBA", (width, height), (255, 255, 255, 0))
        # color_rgba = ImageColor.getcolor(self.blue_color, "RGBA")

        self.draw = ImageDraw.Draw(txt_layer)

        text = "COMUNICADO"
        font = ImageFont.truetype(self.libre_baskerville_font, 120)

        text_width, text_height = self.draw.textbbox((0, 0), text, font=font)[2:]


        # Center the text
        x = (1080 - text_width) // 2
        y = (120 * 2 - text_height) // 2


        self.draw.text((x, y + 850), text, font=font, fill=(0, 0, 0, 0), stroke_width=3, stroke_fill=(self.color_to_use))

        self.image = Image.alpha_composite(self.image, txt_layer)
    
    def create_gradient(self):
        gradient = Image.new('L', (1, self.image.height), color=0xFF)

        for y in range(self.image.height):
            gradient.putpixel((0, -y), int(255 * (1 - 2.5 * float(y)/self.image.height)))


        alpha = gradient.resize(self.image.size)
        black_im = Image.new('RGBA', (self.image.width, self.image.height), color=self.color_to_use)
        black_im.putalpha(alpha)
        gradient_im = Image.alpha_composite(self.image, black_im)


        cropped_image = gradient_im.crop((0, 1, self.image.width, self.image.height))

        return cropped_image
    


    def create_post(self):
        # Create new image based on background image
        self.image = Image.new("RGBA", (self.background_image.width, self.background_image.height), (0, 0, 0, 0))

        self.image.paste(self.background_image, (0, 0))

        self.draw = ImageDraw.Draw(self.image)


        self.draw_centered_white_text('CULTO DE', 120, 140, self.montserrat_arabic_font)

        if self.day_of_the_week == 'SÁBADO':
            self.draw_centered_white_text(self.day_of_the_week, 140, 270, self.libre_baskerville_font)
        else:
            self.draw_centered_white_text(self.day_of_the_week, 140, 250, self.libre_baskerville_font)


        self.draw.rounded_rectangle((300, 560, 780, 650), 20, outline=self.color_to_use, width=5)

        self.draw_centered_white_text(self.date, 50, 555, self.montserrat_medium_font)



        self.draw_text_under_gradient()
        self.image = self.create_gradient()


        self.draw = ImageDraw.Draw(self.image)


        self.draw_centered_white_text(self.theme, 50, 680, self.montserrat_medium_font)
        self.draw_centered_white_text(self.preacher, 50, 750, self.montserrat_medium_font)

        self.image.save(os.path.abspath('app/src/created-images/post.png'), 'PNG')

        return True

    def create_youtube_thumbnail(self):
        self.image = Image.new("RGBA", (1280, 720), (0, 0, 0, 0))

        #Resize background image to fit the tumbnail measures
        resized_bg_image = Image.new("RGBA", (self.background_image.width, self.background_image.height), (0, 0, 0, 0))

        resized_bg_image.paste(self.background_image, (0, 0))

        resized_bg_image = resized_bg_image.resize((1280, 1280))

        self.image.paste(resized_bg_image, (0, 0))



        self.draw = ImageDraw.Draw(self.image)

        self.draw_centered_white_text('CULTO DE', 120, 10, self.montserrat_arabic_font)

        if self.day_of_the_week == 'SÁBADO':
            self.draw_centered_white_text(self.day_of_the_week, 140, 140, self.libre_baskerville_font)
        else:
            self.draw_centered_white_text(self.day_of_the_week, 140, 120, self.libre_baskerville_font)

        
        self.draw.rounded_rectangle((395, 390, 875, 480), 20, outline=self.color_to_use, width=5)

        self.draw_centered_white_text(self.date, 50, 385, self.montserrat_medium_font)

        self.draw_text_under_gradient()
        self.image = self.create_gradient()


        self.draw = ImageDraw.Draw(self.image)


        self.draw_centered_white_text(self.theme, 50, 500, self.montserrat_medium_font)
        self.draw_centered_white_text(self.preacher, 50, 580, self.montserrat_medium_font)

        self.image.save(os.path.abspath('app/src/created-images/thumbnail.png'), 'PNG')

        return True

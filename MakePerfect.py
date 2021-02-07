from PIL import Image, ImageFilter, ImageDraw, ImageFont, ImageColor
import os, random, io, requests, datetime
from discord_webhook import DiscordWebhook
from .. import config as conf
#
drawModeRandom = True
drawMode = 2
drawTextMode = 2

lw = "LW"
W, H = (512,512)

sendToDiscord = True
debug = False

def calculate_brightness(image):
    greyscale_image = image.convert('L')
    histogram = greyscale_image.histogram()
    pixels = sum(histogram)
    brightness = scale = len(histogram)

    for index in range(0, scale):
        ratio = histogram[index] / pixels
        brightness += ratio * (-scale + index)

    return 1 if brightness == 255 else brightness / scale

def random_color(bottomBound, upperBound ):
	random_number = random.randint(bottomBound,upperBound)
	hex_number = str(hex(random_number))
	hex_number = '#'+ hex_number [2:];
	valid_hex = False
	while (not valid_hex):
		if len(hex_number) < 4 or len(hex_number) < 7:
			hex_number = hex_number + str(0);
		else:
			valid_hex = True;
	return hex_number

def generateIcon():
	if (drawModeRandom):
		drawMode = random.randint(1,2)
		drawTextMode = random.randint(1,2)
		
	rand_imagebg = "props/bg/"+random.choice(os.listdir("props/bg/"))

	if drawMode == 2:
		rand_imagebg = io.BytesIO(requests.get("https://source.unsplash.com/random").content)

	img1 = Image.open(rand_imagebg).convert('RGBA')

	cropped = img1.crop((0, 0, 512, 512))

	filters = [ImageFilter.GaussianBlur(radius=5), ImageFilter.BLUR,\
				ImageFilter.CONTOUR, ImageFilter.DETAIL, ImageFilter.EDGE_ENHANCE,\
				ImageFilter.EDGE_ENHANCE_MORE, ImageFilter.EMBOSS,\
				ImageFilter.SHARPEN, ImageFilter.SMOOTH, ImageFilter.SMOOTH_MORE,\
				ImageFilter.UnsharpMask(radius=2, percent=150, threshold=3),\
				ImageFilter.RankFilter(3,0),\
				ImageFilter.MedianFilter(size=3)]
	#img1 = cropped.filter(ImageFilter.GaussianBlur(radius=5))
	random_filter = random.choice(filters);
	img1 = cropped.filter(random_filter)
	img1 = img1.filter(ImageFilter.GaussianBlur(radius=5))
	if drawTextMode == 1:
		rand_imagetext = "props/text/"+random.choice(os.listdir("props/text/"))
		img2 = Image.open(rand_imagetext).convert('RGBA')
		final1 = Image.alpha_composite(img1, img2)
		
	if drawTextMode == 2:
		randFont = "fonts/"+random.choice(os.listdir("fonts/"))
		print(randFont);
		myFont = ImageFont.truetype(randFont, 250)
		draw = ImageDraw.Draw(img1)
		w, h = draw.textsize(lw, font=myFont)
		i = 0;
		while(w+30 > W):
			i = i+1
			myFont = ImageFont.truetype(randFont, 250-i)
			draw = ImageDraw.Draw(img1)
			w, h = draw.textsize(lw, font=myFont)
		while(w < W-70):
			i = i+1
			myFont = ImageFont.truetype(randFont, 250+i)
			draw = ImageDraw.Draw(img1)
			w, h = draw.textsize(lw, font=myFont)
		#print(str(W) + " " + str(w) + " " + str(H) + " " + str(h))
		bright_bg = calculate_brightness(img1);
		print(bright_bg)
		if bright_bg>0.8:
			t_color = random_color(8388600, 16777215) #"#aaa"
			t_back_color = "#777"
		else:
			t_color = random_color(0, 8388600) #"white"
			t_back_color = "#555"
		draw.text(((W-w)/2+5,(H-h)/2+5), lw, fill=t_back_color, font=myFont)
		draw.text(((W-w)/2,(H-h)/2), lw, fill=t_color, font=myFont)
		final1 = img1
		print(t_color)

	final1.save('out/out.png')

	if not sendToDiscord:
		final1.show()
	if(drawTextMode == 2):
		info = str(datetime.datetime.now()) + " \nUsed filter: " + str(random_filter) + "\nUsed font: " + str(randFont) \
			+ "\nGlobal bright level: " + str(bright_bg) + "\nUsed text color: " + str(t_color)
	else:
		info = str(datetime.datetime.now()) + " \nUsed filter: " + str(random_filter) + "\nUsed text-prop: " + rand_imagetext

	if sendToDiscord:
		if debug == False:
			info = ""

		webhook = DiscordWebhook(url=conf.webhook_url,\
								content=info)
		b = io.BytesIO()
		final1.save(b, "PNG")
		b.seek(0)
		webhook.add_file(file=b.read(), filename='logo.png')
		response = webhook.execute()
		print(response)
		
		
		#with open('image.jpg', 'rb') as f:
		#icon = f.read()
		#await bot.edit_server(ctx.message.server, icon=icon)
		
	print(info)
#outimg.save('out/out.png')
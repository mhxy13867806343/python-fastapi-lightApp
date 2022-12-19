from captcha.image import ImageCaptcha,random_color
import string,random

token=string.digits+string.ascii_letters
print(token)

cap=random.sample(token,4)  #随机字符，固定数量
token_str=''.join(cap)      #拼接字符串
print(token_str)
img=ImageCaptcha()          #实例化ImageCaptcha类
#这是ImageCaptcha自带的初始化内容width=160, height=60, fonts=None, font_sizes=None，可以自己设置

RGB=(38,38,0)       #字体色
bgc=(255,255,255)   #背景色
color=random_color(50,180)  #生成随机颜色
image=img.create_captcha_image(token_str,RGB,bgc)
img.create_noise_dots(image=image,color=color,width=10,number=10)
img.create_noise_curve(image=image,color=RGB)
image.save('验证码.png')
print('验证码生成成功',dir(image))
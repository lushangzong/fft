'''
********************************************************
作者：鲁尚宗 时间：2018年11月10日 
本程序实现了傅里叶变换和快速傅里叶变换及其逆变换
图像大小必须为2的整数次幂
*********************************************************
'''
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np

'''
********************************************
DFT,傅里叶变换
最原始的傅里叶计算方法，采用四个循环来计算。
函数参数为数组，计算过程不改变传入参数的数值
返回值为计算的傅里叶变换的数组，类型为complex
********************************************
'''


def my_dft(img_array):
    # 数组的高度和宽度
    height = img_array.shape[0]
    width = img_array.shape[1]

    # 复数的数组用来储存结果
    result_complex = np.zeros([height, width], np.complex64)

    # 遍历每一个像素
    j = complex(0, -1)
    for u in range(height):
        for v in range(width):
            for x in range(height):
                for y in range(width):
                    result_complex[u, v] = result_complex[u, v] + img_array[x, y] * np.exp \
                        (j * 2 * np.pi * (u * x / height + v * y / width))

    # 返回结果
    return result_complex


'''
************************************
IDFT,傅里叶逆变换
最原始的傅里叶逆变换计算方法，采用四个循环来计算。
函数参数为complex数组，计算过程不改变传入参数的数值
返回值为计算的傅里叶变换的数组，类型为float
***************************************
'''


def my_idft(img_array):
    # 数组的高度和宽度
    height = img_array.shape[0]
    width = img_array.shape[1]

    # 创建两个数组，复数的数组用来储存中间结果，浮点数的数组用来计算振幅
    result_complex = np.zeros([height, width], np.complex64)
    result = np.zeros([height, width], np.float64)

    # 遍历每一个像素，先计算复数结果，再对其求振幅
    # 逆变换与正变换的不同之一在于复数的符号
    j = complex(0, 1)
    for u in range(height):
        for v in range(width):
            for x in range(height):
                for y in range(width):
                    result_complex[u, v] = result_complex[u, v] + img_array[x, y] * np.exp \
                        (j * 2 * np.pi * (u * x / height + v * y / width))

            # 逆变换的不同之二在于需要除以一个系数，这个系数由图片的大小决定
            # 正逆变换的系数自洽就行，到底是哪个有系数无所谓，还可以将系数开方拆成两个
            result[u, v] = np.abs(result_complex[u, v] / (height * width))

    # 返回结果
    return result


'''
************************************
FFT,快速傅里叶变换 采用递归实现
函数参数为图像数组，计算过程不改变传入参数的数值
返回值为计算的傅里叶变换的数组，类型为complex
***************************************
'''


def my_fft(img_array):
    # 数组的高度和宽度
    height = img_array.shape[0]
    width = img_array.shape[1]

    # 复数的数组用来储存结果
    result_complex = img_array.astype(np.complex)

    def fft_one(a):
        len = a.size
        if len == 1:  # 递归出口
            return

        # 按照序号的奇偶性分成两部分，减小规模
        a0 = np.zeros(len // 2, complex)
        a1 = np.zeros(len // 2, complex)
        for i in range(0, len, 2):
            a0[i // 2] = a[i]
            a1[i // 2] = a[i + 1]
        fft_one(a0)
        fft_one(a1)

        # 计算原图像的傅里叶变换
        wn = complex(np.cos(2 * np.pi / len), np.sin(2 * np.pi / len))  # 参数
        w = complex(1, 0)
        for i in range(len // 2):
            t = w * a1[i]
            a[i] = a0[i] + t
            a[i + len // 2] = a0[i] - t
            w = w * wn

    # 先对图像的每一行做快速傅里叶变换，再对每一列做快速傅里叶变换
    for i in range(height):
        fft_one(result_complex[i])
    for i in range(width):
        fft_one(result_complex[:, i])

    # 返回结果
    return result_complex


'''
*********************************************
IFFT,快速傅里叶逆变换
函数参数为complex数组，计算过程不改变传入参数的数值
返回值为计算的傅里叶变换的数组，类型为double
逆变换只需要改变参数的值以及最后除以一个系数即可
*********************************************
'''


def my_ifft(img_array):
    # 数组的高度和宽度
    height = img_array.shape[0]
    width = img_array.shape[1]

    # 创建两个数组，复数的数组用来储存中间结果，浮点数的数组用来计算振幅
    result_complex = img_array.astype(np.complex)
    result = np.zeros([height, width], np.float64)

    def ifft_one(a):
        len = a.size
        if len == 1:  # 递归出口
            return

        # 按照序号的奇偶性分成两部分，减小规模
        a0 = np.zeros(len // 2, complex)
        a1 = np.zeros(len // 2, complex)
        for i in range(0, len, 2):
            a0[i // 2] = a[i]
            a1[i // 2] = a[i + 1]
        ifft_one(a0)
        ifft_one(a1)

        # 逆变换与正变换的不同之一在于复数的符号
        wn = complex(np.cos(2 * np.pi / len), -1 * np.sin(2 * np.pi / len))  # 参数
        w = complex(1, 0)
        for i in range(len // 2):
            t = w * a1[i]
            a[i] = a0[i] + t
            a[i + len // 2] = a0[i] - t
            w = w * wn

    # 先对图像的每一行做快速傅里叶变换，再对每一列做快速傅里叶变换
    for i in range(height):
        ifft_one(result_complex[i])
    for i in range(width):
        ifft_one(result_complex[:, i])

    # 逆变换的不同之二在于需要除以一个系数，这个系数由图片的大小决定
    for i in range(height):
        for j in range(width):
            result[i, j] = np.abs(result_complex[i, j] / (height * width))

    # 返回结果
    return result


'''
***************************************
绘制数组的函数，传入一个实数数组，绘制它的图像
array为实数数组，name为图片的名字
***************************************
'''


def draw(array, name):
    plt.imshow(array, plt.cm.gray)
    plt.axis('on')  # 关掉坐标轴为 off
    plt.title(name, fontproperties='SimHei')  # 原始图像 图像题目
    plt.show()


# 打开黑白图像
img = Image.open("dog.bmp")

# 将图像转换为数组，截取合适大小，2的n次幂
img_array = np.array(img)
original = img_array[:8, :8]

# 绘制原始图像
draw(original, '原始图像')

myfft = my_fft(original)
myfft_abs = np.abs(myfft)
center = np.fft.fftshift(myfft_abs)  # 把结果移到中间
draw(center, '快速傅里叶变换')

myifft = my_ifft(myfft)
draw(myifft, '快速傅里叶逆变换')

mydft = my_dft(original)
mydft_abs = np.abs(mydft)  # 因为返回值为复数所以需要取振幅
center = np.fft.fftshift(mydft_abs)  # 把结果移到中间
draw(center, '傅里叶变换')


myidft = my_idft(mydft)
draw(myidft, '傅里叶逆变换')




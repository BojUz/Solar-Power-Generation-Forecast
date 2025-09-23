def getCloudPicture(date ,hour):
    import numpy as np
    import cv2 
    import pyautogui
    import time
    from PIL import Image
    import PIL.ImageOps 
    import datetime
    import requests
    dt = datetime.datetime.strptime(f"{date} {hour}", "%Y-%m-%d %H")
    #dateStr = date.strftime('%d%m%Y_%H')
    day1, month1, year1 = date.split("-")[2], date.split("-")[1], date.split("-")[0]
    dateStr = str(day1) + str(month1) + str(year1)+ "_" + str(hour)
    
    # Добавяме 3 часа
    dt_plus_3 = dt - datetime.timedelta(hours=3)

    date = dt_plus_3.strftime("%Y-%m-%d")
    hour = dt_plus_3.strftime("%H")

    #date = datetime.datetime(2024,6,23,15)
    day, month, year = date.split("-")[2], date.split("-")[1], date.split("-")[0]
    print("#############")
    print(date)
    print(hour)
    ##############
    #2024-06-30
    #21
    
    url = "https://data.ventusky.com/"+str(year)+"/"+str(month)+"/"+str(day)+"/aladin/whole_world/hour_"+str(hour)+"/aladin_oblacnost_"+str(year) + str(month) + str(day)+ "_" + str(hour)+".jpg"
    print(url)
    #url = "https://data.ventusky.com/"+date.strftime('%Y/%m/%d')+"/aladin/whole_world/hour_"+date.strftime('%H')+"/aladin_oblacnost_"+date.strftime('%Y%m%d_%H')+".jpg"
    #url = "https://data.ventusky.com/2025/09/12/aladin/whole_world/hour_03/aladin_oblacnost_20250912_03.jpg"
    filename = "static/aladinImage.jpg"  # името под което ще се запише

    response = requests.get(url)

    if response.status_code == 200:
        with open(filename, "wb") as f:
            f.write(response.content)
        print(f"Изображението е запазено като {filename}")
    else:
        print("Грешка при сваляне:", response.status_code)
    im = Image.open("static/aladinImage.jpg")

    # Setting the points for cropped image
    left = 593
    top = 499 + 9
    right = 773
    bottom = 617 + 9
    #  570 X 375 px
    # Cropped image of above dimension
    # (It will not change original image)
    im1 = im.crop((left, top, right, bottom))
    im1.save("static/image2.png", "png")
    # Shows the image in image viewer
    #im1.show()

    # Create a new alpha mask, initially all white, that makes parts of image transparent
    w, h = 570, 375
    alpha = np.ones((h,w), dtype=np.uint8)*255

    # Draw a vertical black line of length "l" from top downwards at each column position across image
    for row in range(h):
        # Length of line is given by a sine wave
        for col in range(w):
            # croping the sea
            if row>120 and col>520:
                alpha[row, col] = 0
            if row>195 and col>499 and row<255:
                alpha[row, col] = 0
            # croping Turkey
            if w-185<col and h-85<row:
                alpha[row, col] = 0
            if w-219<col and h-57<row:
                alpha[row, col] = 0
            #croping Romania
            if col>67 and col<380 and row<20:
                alpha[row, col] = 0
            if col>67 and col<330 and row<46:
                alpha[row, col] = 0
            if col>140 and col<320 and row<60:
                alpha[row, col] = 0
            if col>420 and row<60 and int(row*1.6)-col<-455:
                alpha[row, col] = 0
            # Croping North Macedonia and Greece
            if col<47 and row>277:
                alpha[row, col] = 0
            if col<257 and row>364:
                alpha[row, col] = 0
            


    # Now open our image and push that alpha layer into it

    # im.show()
    img = cv2.imread("static/image2.png") 

    # Resizing the image 
    image = cv2.resize(img, (570, 375)) 

    # Convert Image to Image HSV 
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV) 

    # Defining lower and upper bound HSV values 106  89 152
    # [0-10],[10-20],[20-30],[30-40],[40-50],[50-60],[60-70],[70-80],[80-90],[90-100]
    # lowerCloudy = [[106,  66, 152],[0, 0,196],[0, 0, 208]]
    # upperCloudy = [[107,  89, 177],[240, 0, 207],[0, 0, 212]]
    # na index 0 e mask1 koqto se poluchava kato se vzeme vsichko, koeto ne e oblak i sled tova
    #izobrajenieto si invertira cvetovete
    lowerCloudy = [[0, 0, 0],[0, 0, 35],[0, 0, 95]]
    upperCloudy = [[1, 1, 8],[1, 1, 95],[1, 1, 255]]
    lower = np.array(lowerCloudy[0]) 
    upper = np.array(upperCloudy[0]) 

    # Defining mask for detecting color 
    mask = cv2.inRange(hsv, lower, upper) 

    # Display Image and Mask 
    # cv2.imshow("Image", image) 
    # cv2.imshow("Mask", mask) 
    cv2.imwrite("static/mask.png", mask)

    lower = np.array(lowerCloudy[2]) 
    upper = np.array(upperCloudy[2]) 
    mask2 = cv2.inRange(hsv, lower, upper) 

    # Display Image and Mask 
    # cv2.imshow("Image", image) 
    # cv2.imshow("Mask2", mask2) 
    cv2.imwrite("static/mask2.png", mask2)

    lower = np.array(lowerCloudy[1]) 
    upper = np.array(upperCloudy[1]) 
    mask4 = cv2.inRange(hsv, lower, upper) 
    cv2.imwrite("static/mask4.png", mask4)

    ####################
    #ot = cv2.imread("static/output.png") 
    #ot = cv2.resize(ot, (570, 375)) 
    #cv2.imwrite("static/output.png", ot)

    #img = Image.open("static/outputInv.png").convert("RGB")
    ######################
    mask1 = Image.open('static/mask.png').convert('RGB')
    mask1.putalpha(Image.fromarray(alpha))
    ####################
    #mask1.save('static/result.png')
    # im.show()
    #img.putalpha(Image.fromarray(alpha))
    #img.save('static/outputInv.png')
    # img.show()
    ##################

    mask2 = Image.open('static/mask2.png').convert('RGB')
    mask2.putalpha(Image.fromarray(alpha))
    mask2.save('static/mask2.png')



    mask2 = Image.open('static/mask2.png')
    if mask2.mode == 'RGBA':
        r,g,b,a = mask2.split()
        rgb_image = Image.merge('RGB', (r,g,b))

        inverted_image = PIL.ImageOps.invert(rgb_image)

        r2,g2,b2 = inverted_image.split()

        final_transparent_image = Image.merge('RGBA', (r2,g2,b2,a))

        final_transparent_image.save('static/mask2.png')

    else:
        inverted_image = PIL.ImageOps.invert(mask2)
        inverted_image.save('static/mask2.png')


    mask4 = Image.open('static/mask4.png')
    if mask4.mode == 'RGBA':
        r,g,b,a = mask4.split()
        rgb_image = Image.merge('RGB', (r,g,b))

        inverted_image = PIL.ImageOps.invert(rgb_image)

        r2,g2,b2 = inverted_image.split()

        final_transparent_image = Image.merge('RGBA', (r2,g2,b2,a))

        final_transparent_image.save('static/mask4.png')

    else:
        inverted_image = PIL.ImageOps.invert(mask4)
        inverted_image.save('static/mask4.png')


    ###########3
    #x, y = img.size
    ###########





    # Read the image 
    src = cv2.imread("static/mask.png", 1) 

    # Convert image to image gray 
    tmp = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY) 

    # Applying thresholding technique 
    _, alpha2 = cv2.threshold(tmp, 0, 255, cv2.THRESH_BINARY) 

    # Using cv2.split() to split channels 
    # of coloured image 
    b, g, r = cv2.split(src) 

    # Making list of Red, Green, Blue 
    # Channels and alpha 
    rgba = [b, g, r, alpha2] 

    # Using cv2.merge() to merge rgba 
    # into a coloured/multi-channeled image 
    dst = cv2.merge(rgba, 4) 

    # Writing and saving to a new image 
    cv2.imwrite("static/mask.png", dst) 


    src = cv2.imread("static/mask2.png", 1) 

    # Convert image to image gray 
    tmp = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY) 

    # Applying thresholding technique 
    _, alpha2 = cv2.threshold(tmp, 0, 255, cv2.THRESH_BINARY) 

    # Using cv2.split() to split channels 
    # of coloured image 
    b, g, r = cv2.split(src) 

    # Making list of Red, Green, Blue 
    # Channels and alpha 
    rgba = [b, g, r, alpha2] 

    # Using cv2.merge() to merge rgba 
    # into a coloured/multi-channeled image 
    dst = cv2.merge(rgba, 4) 

    # Writing and saving to a new image 
    cv2.imwrite("static/mask2.png", dst) 




    src = cv2.imread("static/mask4.png", 1) 

    # Convert image to image gray 
    tmp = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY) 

    # Applying thresholding technique 
    _, alpha2 = cv2.threshold(tmp, 0, 255, cv2.THRESH_BINARY) 

    # Using cv2.split() to split channels 
    # of coloured image 
    b, g, r = cv2.split(src) 

    # Making list of Red, Green, Blue 
    # Channels and alpha 
    rgba = [b, g, r, alpha2] 

    # Using cv2.merge() to merge rgba 
    # into a coloured/multi-channeled image 
    dst = cv2.merge(rgba, 4) 

    # Writing and saving to a new image 
    cv2.imwrite("static/mask4.png", dst) 




    mask1 = Image.open('static/mask.png').convert('RGB')
    mask1.putalpha(Image.fromarray(alpha))
    mask2 = Image.open('static/mask2.png').convert('RGB')
    mask2.putalpha(Image.fromarray(alpha))
    mask4 = Image.open('static/mask4.png').convert('RGB')
    mask4.putalpha(Image.fromarray(alpha))
    # mask2.save('static/mask2.png')
    # mask1.save('static/mask.png')

    background = Image.open("static/BlackBackground.png")
    mask2.paste(background,(0,0), mask =background)
    mask1.paste(background,(0,0), mask =background)
    mask4 = Image.open("static/mask4.png")
    mask4.paste(background,(0,0), mask =background)
    # img1.paste(img2, (0,0), mask = img2) 
    mask1.save('static/mask.png')
    mask2.save("static/mask2.png")
    mask4.save("static/mask4.png")
    img = Image.open('static/mask2.png') 
    rgba = img.convert("RGBA") 
    datas = rgba.getdata() 

    newData = [] 
    for item in datas: 
        if item[0] != 0 and item[1] != 0 and item[2] != 0:  # finding black colour by its RGB value 
            # storing a transparent value when we find a black colour 
            newData.append((255, 255, 255, 0)) 
        else: 
            newData.append(item)  # other colours remain unchanged 

    rgba.putdata(newData) 
    rgba.save("static/mask2.png", "PNG") 
    mask1 =Image.open('static/mask.png')
    mask1.putalpha(95)
    mask1.save("static/mask.png")
    mask4 =Image.open('static/mask4.png')
    mask4.putalpha(190)
    mask4.save("static/mask4.png")
    mask3= Image.open('static/mask.png')
    # Half alpha; alpha argument must be an int
    mask3.putalpha(130)

    mask3.save("static/mask3.png")
    img = Image.open('static/mask.png') 
    rgba = img.convert("RGBA") 
    datas = rgba.getdata() 

    newData = [] 
    for item in datas: 
        if item[0] != 0 and item[1] != 0 and item[2] != 0:  # finding black colour by its RGB value 
            # storing a transparent value when we find a black colour 
            newData.append((255, 255, 255, 0)) 
        else: 
            newData.append(item)  # other colours remain unchanged 

    rgba.putdata(newData) 
    rgba.save("static/mask.png", "PNG") 

    img = Image.open('static/mask3.png') 
    rgba = img.convert("RGBA") 
    datas = rgba.getdata() 

    newData = [] 
    for item in datas: 
        if item[0] != 0 and item[1] != 0 and item[2] != 0:  # finding black colour by its RGB value 
            # storing a transparent value when we find a black colour 
            newData.append((255, 255, 255, 0)) 
        else: 
            newData.append(item)  # other colours remain unchanged 

    rgba.putdata(newData) 
    rgba.save("static/mask3.png", "PNG") 



    img = Image.open('static/mask4.png') 
    rgba = img.convert("RGBA") 
    datas = rgba.getdata() 

    newData = [] 
    for item in datas: 
        if item[0] != 0 and item[1] != 0 and item[2] != 0:  # finding black colour by its RGB value 
            # storing a transparent value when we find a black colour 
            newData.append((255, 255, 255, 0)) 
        else: 
            newData.append(item)  # other colours remain unchanged 

    rgba.putdata(newData) 
    rgba.save("static/mask4.png", "PNG") 


    mask1 = Image.open('static/mask.png')
    mask2 = Image.open('static/mask2.png')
    mask3 = Image.open('static/mask3.png')
    mask4 = Image.open('static/mask4.png')
    img = Image.open("static/outputBW2.png")
    #############
    #imgOpacity = Image.open("outputBW2.png")
    #########3

    img.paste(mask2, (0,0), mask = mask2)
    img.paste(mask1, (0,0), mask = mask1)
    img.paste(mask4, (0,0), mask = mask4) 
    ##############################################################
    #den na komentar 18.08.2025 - dolnite 3 reda + zapazvaneto na imgOpacity po dolu gi zakomeniram
    #imgOpacity.paste(mask2, (0,0), mask = mask2)
    #imgOpacity.paste(mask3, (0,0), mask = mask3)
    #imgOpacity.paste(mask4, (0,0), mask = mask4) 
    ##############################################################

    # img3 = Image.blend(mask1,img, 0.9)
    # img3 = Image.blend(img3, mask2, 0,2)
    #img.show()

    img.save("static/images/result_"+dateStr+".png")
    ######################################
    #imgOpacity.save("resultOpacity130.png")
    ######################################

    # Make python sleep for unlimited time 
    # cv2.waitKey(0) 
    ###############################
    '''
    i=i+1
    date += datetime.timedelta(hours=3)
    internetCon = False
    timeOutInternet = 0
    while internetCon == False:
        try:
            res = requests.get("https://www.ventusky.com/?p=42.71;25.98;6&l=clouds-total&t=20240706/0000&m=aladin&w=off")
            if res.status_code == 200:
                internetCon = True
        except:
            timeOutInternet = timeOutInternet + 1
            if(timeOutInternet>=90):
                print("No internet: ",datetime.datetime.now())
                timeOutInternet=1
    pyautogui.press('right')
    time.sleep(1)
    if(date.hour==21):
        date += datetime.timedelta(hours=9)
        pyautogui.press('right')
        time.sleep(1)
        pyautogui.press('right')
        time.sleep(1)
        pyautogui.press('right')
        time.sleep(2)
        
    dateStr = date.strftime('%d%m%Y_%H')
    # 5hours by 17 days

    print(dateStr)'''
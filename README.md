<h3 align="center">Wireless DNA Hackathon</h3>

<!-- The Challenge -->

## The Challenge
Doppler Radio Interference is a type of radio interference that occurs when a radio signal is reflected by a moving object, 
such as a vehicle, a person, or a weather balloon. This results in a change in frequency of the reflected signal, which can
cause interference with other radio signals that are operating in the same frequency band.

Radio interferences can be either stable or changing both in time and space and typically have a radial shape. Artificial Intelligence image processing can be used to extract clean data from these interferences. Detecting the interferences is crucial in eliminating them, and this becomes more complicated when the radar is detecting rain, as the rain pattern must be reconstructed accurately in terms of both shape and values. The final outcome should be a numerical data file in netCDF format that contains corrected radar data.

The main file is ```full.py```, which consists the whole code. This code goes through the custom use_cases folder and gets all images for three radars. Joins them with the ```overlap``` function and corrects the interference with the ```remove_interferences``` function. In the end it saves processed images in joined folder. Also with the function ```create_ncdf``` it saves the data in myfile.nc file. 

Below you can see some examples of our processed data. In the left, it shows the overlapped images, while the right demonstrates the picture with our 

![image](https://user-images.githubusercontent.com/35425540/218045983-9147788b-e9b4-468b-ba9e-7885aa0e2255.png)

![image](https://user-images.githubusercontent.com/35425540/218046775-ff361827-e8bd-48d3-86f7-b147655c446b.png)

![image](https://user-images.githubusercontent.com/35425540/218046861-e620cba7-d9c6-4c55-a0b2-96fb46429f34.png)



## Team members

* Aicha Moussaid
* Sherkhan Azimov
* SM Zahid Hasan
* Lunara Nurgaliyeva
* Dariya
* Modlir


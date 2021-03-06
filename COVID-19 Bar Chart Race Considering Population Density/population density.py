import kaggle
import shutil
import os
import pandas as pd
import matplotlib.pyplot as plt
import cv2
import numpy as np
from PIL import Image
FourCC=cv2.VideoWriter_fourcc('m','p','4','v')
video=cv2.VideoWriter('Bar Chart Race (Population density).mp4',FourCC,30,(1920,1080))
def directories():
	if os.path.exists('Dataset'):
		shutil.rmtree('Dataset')
	os.makedirs('Dataset')
	if os.path.exists('Frames'):
		shutil.rmtree('Frames')
	os.makedirs('Frames')
	print('\nDirectories created successfully !!!')
def directories_2():
	if os.path.exists('Dataset'):
		shutil.rmtree('Dataset')
	if os.path.exists('Frames'):
		shutil.rmtree('Frames')
	os.remove('template.png')
	print('\nDirectories deleted successfully !!!')
def download():
	#C:\Users\<username>\.kaggle
	kaggle.api.authenticate()
	kaggle.api.dataset_download_files('sudalairajkumar/novel-corona-virus-2019-dataset',path='Dataset',unzip=True)
	kaggle.api.dataset_download_files('tanuprabhu/population-by-country-2020',path='Dataset',unzip=True)
	print('\nDownloads successful !!!')#Executed only if there wasnt an error in downloading
def process(key):
	if key=='confirmed':
		template=np.full(shape=(1080,1920,3),fill_value=(255,255,204),dtype=np.uint8)#BGR
		color=(0,0,1)#RGB
		face_color=(0.8,1,1)#RGB
		SubHeading='(Number of confirmed cases) x (population density)'
	elif key=='recovered':
		template=np.full(shape=(1080,1920,3),fill_value=(179,255,179),dtype=np.uint8)
		color=(0,1,0)
		face_color=(0.7,1,0.7)
		SubHeading='(Number of recovered cases) x (population density)'
	else:
		template=np.full(shape=(1080,1920,3),fill_value=(179,179,255),dtype=np.uint8)
		color=(1,0,0)
		face_color=(1,0.7,0.7)
		SubHeading='(Number of deaths) x (population density)'
	cv2.imwrite('template.png',template)
	Dataset=pd.read_csv(os.path.join('Dataset','time_series_covid_19_'+key+'.csv'))
	#print(Dataset.head(20))
	Dates=Dataset.columns[4:]
	Countries=[i for i in Dataset.loc[:,'Country/Region'].unique()]
	Count=0
	last=len(Dates)
	for Date in Dates:
		Count+=1
		Cases=[]
		temp=[]
		for i in Countries:
			dataset=Dataset[Dataset['Country/Region']==i]
			total_value=dataset[Date].sum()
			if i=='US':
				i='United States'
			elif i=='Korea, South':
				i='South Korea'
			elif i=='Cote d\'Ivoire':
				i='Côte d\'Ivoire'
			elif i=='Czechia':
				i='Czech Republic (Czechia)'
			elif i=='Taiwan*':
				i='Taiwan'
			elif i=='Burma':
				i='Myanmar'
			elif i=='Sao Tome and Principe':
				i='Sao Tome & Principe'
			elif i=='Congo (Brazzaville)':
				i='Congo'
			elif i=='Congo (Kinshasa)':
				i='DR Congo'
			elif i=='Saint Vincent and the Grenadines':
				i='St. Vincent & Grenadines'
			elif i=='Saint Kitts and Nevis':
				i='Saint Kitts & Nevis'
			flag=0
			for j in range(len(Dataset_Density)):
				if i==Dataset_Density.iloc[j,0]:
					total_value*=Dataset_Density.iloc[j,4]
					Cases.append(total_value)
					temp.append(i)
					flag=1
					break
			if flag==0:
				if i=='Kosovo':
					total_value*=159
					Cases.append(total_value)
					temp.append(i)
				elif i=='West Bank and Gaza':
					total_value*=759
					Cases.append(total_value)
					temp.append(i)
				else:
					print('\n\t\tNot Found: ',i)
		Countries=temp
		#MM/DD/YY format ------------> DD/MM/YY format
		temp_list=Date.split('/')
		temp=temp_list[0]
		temp_list[0]=temp_list[1]
		temp_list[1]=temp
		Date='/'.join(temp_list)
		Data=pd.DataFrame({'Countries':Countries,Date:Cases})
		Data.sort_values(by=Date,ascending=False,inplace=True)
		#print(Data.head(7),'\n\n')
		Data=Data.iloc[:7,:]
		Data.sort_values(by=Date,ascending=True,inplace=True)
		plt.barh([i[:20] for i in Data['Countries']],Data[Date],color=color)
		plt.axis('off')
		plt.savefig(os.path.join('Frames','frame.png'),transparent=True,bbox_inches='tight',dpi=300,facecolor=face_color)
		plt.close()
		template=cv2.imread('template.png')
		IMAGE=cv2.imread(os.path.join('Frames','frame.png'))
		IMAGE=Image.fromarray(IMAGE,'RGB')
		IMAGE=IMAGE.resize((1320,800))
		IMAGE=np.array(IMAGE)
		origin_x=480
		origin_y=190
		for i in range(origin_y,origin_y+IMAGE.shape[0]):
			for j in range(origin_x,origin_x+IMAGE.shape[1]):
				template[i][j]=IMAGE[i-origin_y][j-origin_x]
		for i in range(1,8):
			cv2.putText(template,Data.iloc[7-i,0].rjust(16,' ').replace('*',' '),(150,200+100*i),cv2.FONT_HERSHEY_COMPLEX,1,(0,0,0),2)
			cv2.putText(template,str(Data.iloc[7-i,1]).rjust(10,' '),(650,200+i*100),cv2.FONT_HERSHEY_COMPLEX,1,(0,0,0),2)
		cv2.putText(template,Date,(150,110),cv2.FONT_HERSHEY_TRIPLEX,2,(0,0,0),2)
		cv2.putText(template,'COVID-19 Bar Chart Race',(650,110),cv2.FONT_HERSHEY_TRIPLEX,2,(0,0,0),2)
		cv2.putText(template,SubHeading,(635,170),cv2.FONT_HERSHEY_COMPLEX,1,(0,0,0),2)
		for i in range(10):
			video.write(template)
		print('\nFininshed processing: '+str(Count)+'/'+str(last)+' ['+key+']')
		#plt.show()
		#break
	for i in range(75):
		video.write(template)
KEYS=('confirmed','recovered','deaths')
directories()
download()
Dataset_Density=pd.read_csv(os.path.join('Dataset','population_by_country_2020.csv'))
for key in KEYS:
	process(key)
video.release()
directories_2()





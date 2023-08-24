class Info:
	def __init__(self):
		self.surname=None
		self.name=None
		self.patronymic=None
		self.company=None
		self.work_number=None
		self.own_number=None
	def __init__(self,surname:str='',name:str='',patronymic:str='',company:str='',work_number:str='',own_number:str=''):
		self.surname=surname
		self.name=name
		self.patronymic=patronymic
		self.company=company
		self.work_number=work_number
		self.own_number=own_number
	
	def __str__(self):
		return f"{self.surname:15} {self.name:10} {self.patronymic:15} {self.company:30} {self.work_number:20} {self.own_number:20}"
	def __repr__(self):
		return f"{self.surname:15} {self.name:10} {self.patronymic:15} {self.company:30} {self.work_number:20} {self.own_number:20}"


PAGE_SIZE:int=10
page_number:int=0
#объект, использующийся для шапки вывода данных
ex:Info=Info("surname","name","patronymic","company","work_number","own_number")

#Функция для постраничного вывода данных переданного списка, для реализации постраничности используется переменная page_number
def output_info(info:list)->None:
	global page_number
	print('       ',ex)
	print("_"*110)
	for i,item in enumerate(info[page_number*PAGE_SIZE:(page_number+1)*PAGE_SIZE]):
			print(f'{i+page_number*PAGE_SIZE:5}','|',item)
	print(f"Страница {page_number+1} из {len(info)//PAGE_SIZE+1}")
	choice=input("1 - предыдущая страница, 2 - следующая, любой другой символ - закончить просмотр:")
	if (choice=="1"):
		page_number-= 1 if page_number>0 else 0
		output_info(info)
	elif (choice=='2'):
		page_number+= 1 if page_number<len(info)//PAGE_SIZE else 0
		output_info(info)
	else:
		pass		

#Функция для чтения файла с данными, возвращает список объектов, представляющих данные
def read_file(path:str)->list:
	with open(path,encoding='utf-8') as file:
		output=[]
		while (True):
			raw_info=file.readline().split()
			if (not raw_info):
				break
			
			temp_info=Info(*raw_info)
			output.append(temp_info)
		return output

#Функция, реализующая добавление данных
def add_info(info:list)->None:
	data=input("введите необходимые данные через пробел ():").split()
	new_info=Info(*data)
	info.append(new_info)
	print("Добавлено")

#Функция изменения записей, реализована как полная перезапись, так и выбор одного поля для изменения	
def change_info(index:int,info:list)->None:
	choice=input('1 - изменить все поля записи, 2 - одно поле:')
	if choice=='1':
		data=input("Введите новые данные через пробел").split()
		info[index]=Info(*data)
		print("Данные изменены")
	elif choice=='2':
		print("Введите название изменяемого поля")
		print(ex)
		field=input()
		new_value=input("Введите новое значение:")
		info[index].__dict__[field]=new_value
		print("Данные изменены")

"""
Функция поиска
В качестве параметров принимает поле по которому производится поиск и значение этого поля
Поиск производится по включению строки запроса в строки записей
(Поиск реализован прохождением по всем элементам списка, так как записей не будет большое кол-во и это не должно негативно сказаться на производительности)
"""
def find_info(field:str,query:str,info:list)->set:
	temp=set()
	for i,item in enumerate(info):
		if query in item.__dict__[field].lower():
			temp.add(item)
	return temp

"""
Функция, реализующая поиск по нескольким полям записи
Реадизована с помощью пересечения множеств, полученных из поиска по одному из полей
"""
def execute_query(info:list,query:str)->list:
	ans=set()
	for i in query.split(','):
		i=i.lstrip().rstrip()
		field=i[:i.index("=")].lstrip().rstrip().lower()
		query=i[i.index("=")+1:].lstrip().rstrip().lower()
		
		if len(ans)==0:
			ans=ans.union(find_info(field=field,query=query,info=info))
		else:
			ans=ans.intersection(find_info(field=field,query=query,info=info))
	return list(ans)
#Сохранение данных в файл
def save_info(info:list,path:str):
	with open(path,mode="w",encoding="utf-8") as file:
		for i in info:
			file.write(str(i)+'\n')

#Возможность пользователя выбрать путь к файлу справочника
path=input("Введите путь к файлу справочника,либо оставьте пустым для открытия файла по умолчанию.")	
if not path:
	path="file.txt"	
info=read_file(path)

while (True):
	query=input("Введите 1,чтобы вывести все записи на экран,2- чтобы добавить запись,3-изменение записи,4-поиск. Любой другой символ чтобы завершить работу программы и сохранить файл.\n")
	if query=="1":
		output_info(info)
	elif query=="2":
		add_info(info)
	elif query=="3":
		index=input("Введите индекс редактируемой записи:")
		change_info(int(index),info)
	elif query=="4":
		query=input("Введите поисковый запрос в виде поле1=значение1,поле2=значение2... \n")
		output_info(execute_query(query=query, info=info))
	else:
		print("Завершение работы..")
		save_info(info=info,path=path)
		break
		
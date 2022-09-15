
# print('输出x_test文本向量：')
# print(x_test_weight)


# db = pymysql.connect(host='localhost', user='root',
#                      password='121522734a', port=3306, db='Enclusiv')
# cursor = db.cursor()


# cursor.execute("select article.id, user.name from article, user where article.author_id=user.id")


# for article in cursor.fetchall():
# 	cursor.execute("select title from bilibili_article where author=%s", article[1])
# 	title = cursor.fetchone()[0]
# 	cursor.execute("update article set title=%s where id=%s", (title, article[0]))

# db.commit()


"""get img type"""
# cursor.execute("select id, type from image")

# for img in cursor.fetchall():
# 	img_type = img[1].split('.')[1]
# 	print(img_type)
# 	cursor.execute("update image set type=%s where id=%s", (img_type, img[0]))

# db.commit()


"""rename img"""
# cursor.execute("select id, user_id, path from image")

# c = 0
# for img in cursor.fetchall():
# 	if os.path.exists(img[2]):
# 		path = "UserImageSpace/" + str(img[1]) + "/" + str(img[0]) + "." + img[2].split(".")[-1]
# 		os.rename(img[2], path)
# 		# print(path)
# 		cursor.execute("update image set path=%s where id=%s", (path, img[0]))
		
# 	c += 1
# 	if c % 100 == 0:
# 		db.commit()
# 		print(c)


"""replace img name in md"""
# def replace_name(article, ids):
#     lines = []
#     line = ""
#     for i in article:
#         if i != '\n':
#             line += i
#         else:
#             lines.append(line + "\n")
#             line = ""
#     img_num = 0
#     for i in range(len(lines)):
#         if '<img src="' in lines[i]:
#             lines[i] = lines[i].replace(
#                 '<img src="' + str(img_num) + ".", '<img src="' + str(ids[img_num]) + ".")
#             img_num += 1
    
#     article = ""
#     for line in lines:
#         article += line
    
#     return article


# db = pymysql.connect(host='localhost', user='root',
#                      password='121522734a', port=3306, db='Enclusiv')
# cursor = db.cursor()

# cursor.execute("select id, article from article")

# for article in cursor.fetchall():
#     cursor.execute(
#         "select image_id from article_image where article_id=%s", article[0])
#     img_ids = [i[0] for i in cursor.fetchall()]
#     if len(img_ids) > 0:
#         modified = replace_name(article[1], img_ids)
#         cursor.execute("update article set article=%s where id=%s", (modified, article[0]))
#         db.commit()
#     print(article[0])



"""insert img"""
# cursor.execute("select id, author, article, img_paths from bilibili_article")

# article_id = 1
# for article_info in cursor.fetchall():
#     cursor.execute("select id from user where name=%s", article_info[1])
#     author_id = cursor.fetchone()[0]

#     cursor.execute("insert into article (id, author_id, article) values(%s, %s, %s)", (article_id, author_id, article_info[2]))

#     if article_info[3] is not None:
#         img_paths = article_info[3].split(", ")
#         img_paths[0] = img_paths[0][1:]
#         img_paths[len(img_paths) - 1] = img_paths[len(img_paths) - 1][:-1]
#         if article_info[3] != "[]":
#             for path in img_paths:
#                 cursor.execute("select id from image where path=%s", path)
#                 img_id = cursor.fetchone()[0]
#                 cursor.execute("insert into article_image (article_id, image_id) values (%s, %s)", (article_id, img_id))

#     db.commit()
#     article_id += 1
#     print(article_id)

"""txt to markdown"""
# cursor.execute("select id, article, img_paths from bilibili_article")

# data = cursor.fetchall()

# for index in range(len(data)):

#     lines = []

#     line = ""
#     for i in data[index][1]:
#         if i != '\n':
#             line += i
#         else:
#             lines.append(line + "\n")
#             line = ""

#     if data[index][2] is not None:
#         imgs = data[index][2].split(", ")
#         imgs[0] = imgs[0][1:]
#         imgs[len(imgs) - 1] = imgs[len(imgs) - 1][:-1]


#         # print(len(imgs), len(lines))
#         if len(imgs) < len(lines):
#             skip = len(lines) // len(imgs)
#         else:
#             skip = 1


#         offset = 0
#         path_index = 0
#         for i in range(skip - 1, len(lines), skip):
#             if path_index == len(imgs):
#                 break
#             lines.insert(i + offset, '<img src="' + imgs[path_index].split("/")[-1] + '" />\n')
#             offset += 1
#             path_index += 1

#         if offset < len(imgs):
#             for i in range(0, len(imgs) - offset):
#                 lines.append('<img src="' + imgs[path_index].split("/")[-1] + '" />\n')
#                 path_index += 1


#     for i in range(len(lines), 0, -1):
#         lines.insert(i, '\n')

#     article = ""
#     for line in lines:
#         article += line

#     print(index)

#     # if index == 5:
#     #     print(article, end="")
#     #     break


#     cursor.execute("update bilibili_article set article=%s where id=%s", (article, data[index][0]))

# db.commit()


"""fix wrong url"""
# normal_url = "https://i0.hdslb.com/bfs/article/0b977d80ae2d22aac63a0544898cf22cb2019889.jpg"

# data = eval(open("new_data.txt", "r").read())


# for user_id, articles in data.items():
# 	for article_id, img_urls in articles.items():
# 		for i in range(len(img_urls)):
# 			if len(img_urls[i]) != len(normal_url):
# 				if img_urls[i][:10] == "https:http":
# 					proccessed = img_urls[i][6:]
# 					if proccessed[-4:] == 'webp':
# 						j = 0
# 						for c in proccessed:
# 							if c == '@':
# 								break
# 							j+=1
# 						proccessed = proccessed[:j]
# 					img_urls[i] = proccessed
# 				print(i)

# with open("new_data.txt", "w") as f:
#   	f.write(json.dumps(data))


"""create user img path"""
# data = eval(open("new_data.txt", "r").read())

# for id in data.keys():
# 	os.makedirs("UserImageSpace/" + str(id))


"""delete user that without img"""
# data = eval(open("new_data.txt", "r").read())

# print(len(data.keys()))

# user_without_img = []

# for user_id, articles in data.items():
# 	img_num = 0
# 	for article_id, img_urls in articles.items():
# 		img_num += len(img_urls)

# 	if img_num == 0:
# 		user_without_img.append(user_id)

# print(len(user_without_img))


# new_data = {}

# for user_id, articles in data.items():
# 	if user_id not in user_without_img:
# 		new_data[user_id] = articles

# print(len(new_data.keys()))

# with open("new_data.txt", "w") as f:
#  	f.write(json.dumps(new_data))


"""user article imgs"""
# cursor.execute("select id, name from user")

# user_info = cursor.fetchall()[1:]

# data = {}

# for user in user_info:

# 	cursor.execute("select id, img_urls from bilibili_article where author=%s", user[1])

# 	for article in cursor.fetchall():
# 		articles = data.get(user[0], {})
# 		if article[1] != None:
# 			articles[article[0]] = eval(article[1])
# 		else:
# 			articles[article[0]] = []
# 		data.setdefault(user[0], articles)


# with open("data.txt", "w") as  f:
# 	f.write(json.dumps(data))


"""重复 title"""
# cursor.execute("select id, title from bilibili_article")

# titles = {}

# for data in cursor.fetchall():
# 	ids = titles.get(data[1], [])
# 	ids.append(data[0])
# 	titles.setdefault(data[1], ids)


# for title, ids in titles.items():
# 	if len(ids) > 1:
# 		print(title, ids)
# 		for i in range(len(ids)):
# 			cursor.execute("update bilibili_article set title=%s where id=%s", (title + "(" + str(i) + ")", ids[i]))

# db.commit()


"""insert user"""
# cursor.execute("select author, profile_img_url from bilibili_article")

# data = set(cursor.fetchall())

# print(len(data))

# data = list(data)

# base_email = 154871272

# for i in range(len(data)):

# 	cursor.execute(
# 		"insert into user (name, email, password) values (%s, %s, %s)",
# 		(data[i][0], str(base_email + i) + "@qq.com", "123456")
# 		)

# db.commit()


"""parse bilibili"""
# base_url = "https://www.bilibili.com/read/cv"

# index = 1000004


# for i in range(10000):

# 	soup = BeautifulSoup(requests.get(base_url + str(index)).text, 'lxml')

# 	title = soup.find(name="h1");

# 	if title == None:
# 		print(index)
# 	else:
# 		print(index)

# 	index += 1


# db = pymysql.connect(host='localhost', user='root', password='121522734a', port=3306, db='Enclusiv')
# cursor = db.cursor()


# cursor.execute("select * from bilibili_article")

# data = set([i[1:] for i in cursor.fetchall()])


# for i in data:
# 	cursor.execute(
# 				"insert into bilibili_article_copy1 (title, author, profile_img_url, article, img_urls) values (%s, %s, %s, %s, %s)",
# 				i
# 			)

# db.commit()

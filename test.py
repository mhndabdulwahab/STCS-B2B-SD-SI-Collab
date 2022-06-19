# FirstField="11"
# SecondField="287"
# Range="4..."
# cluster = "shared"
# if cluster == "shared":
#         shared="\+966" + FirstField + SecondField
# else:
#     shared = ""

# #x = "rule 2 /^"+Range+"/" " /"+SecondField+"\\"+"0/"   
# x= "rule 2 /^"+FirstField + SecondField+""+"\\"+"("+Range+""+"\\"+")/ /"+shared+"\\"+"1/"
# print(x)

ThirdFieldR2="1099"
ThirdField="1000"
# if (ThirdFieldR2) - (ThirdField) >= 999:
#         ThirdFieldRange = (ThirdFieldR2)/1000
#         Range=str(int(ThirdFieldRange))+"...$"
# elif  (ThirdFieldR2) - (ThirdField) >= 99:
#         ThirdFieldRange = (ThirdFieldR2)/100
#         Range=str(int(ThirdFieldRange))+"..$"
# # print(Range)



if int(ThirdFieldR2) - int(ThirdField) >= 999:
        ThirdFieldRange = int(ThirdFieldR2)/1000
        Range=str(int(ThirdFieldRange))+"...$"
elif  int(ThirdFieldR2) - int(ThirdField) >= 99:
        ThirdFieldRange = int(ThirdFieldR2)/100
        Range=str(int(ThirdFieldRange))+"..$"
print(Range)




# if (ThirdFieldR2) - (ThirdField) >= 999:
#         ThirdFieldRange = (ThirdFieldR2)/1000
#         Range=str(((ThirdFieldRange)))+"...$"
# elif  (ThirdFieldR2) - (ThirdField) >= 99:
#         ThirdFieldRange = ((ThirdFieldR2))/100
#         Range=str((ThirdFieldRange))+"..$"





    # "rule 1 /^"+SecondField+""+"\\"+"("+Range+""+"\\"+")/ /"+HcsShareDilledNumber+"\\"+"1/ ", 




    #     if int(ThirdFieldR2) - int(ThirdField) >= 999:
    #     ThirdFieldRange = int(ThirdFieldR2)/1000
    #     Range=str(int(float(ThirdFieldRange)))+"...$"
    # elif  int(ThirdFieldR2) - int(ThirdField) >= 99:
    #     ThirdFieldRange = int((ThirdFieldR2))/100
    #     Range=str(int(ThirdFieldRange))+"..$"




#      if hosted == "Hosted_collab_solution":
#         if cluster =="shared_cluster":
#             HcsShareDilledNumber = "\+966" + FirstField + SecondField
#         else:
#             HcsShareDilledNumber = ""


#     else:
#         HcsShareDilledNumber=""


#  if hosted == "Hosted_collab_solution":
#         if cluster =="shared_cluster":
#             HcsShareDilledNumber = "\+966" + FirstField + SecondField
#         else:
#             HcsShareDilledNumber = ""


#     else:

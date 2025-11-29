import matplotlib.pyplot as plt

categories = ['apple','banana','pineapple']
values = [15,20,10]

plt.pie(values,labels=categories,autopct="%1.2f%%")
plt.show()

# # save picture 
plt.savefig('piechart.png', dpi=300, bbox_inches='tight', transparent=False)

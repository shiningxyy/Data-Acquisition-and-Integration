import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

element=pd.read_excel('element.xlsx')
age=pd.read_excel('age.xlsx')
strength=pd.read_excel('strength.xlsx')

strength.rename(columns={'serial_number': 'number'}, inplace=True)
strength.rename(columns={'Concrete compressive strength(MPa, megapascals) ': 'Concrete compressive strength'}, inplace=True)
age.rename(columns={'No.': 'number'}, inplace=True)
element.rename(columns={'Cement (component 1)(kg in a m^3 mixture)':'Cement'}, inplace=True)
element.rename(columns={'Blast Furnace Slag (component 2)(kg in a m^3 mixture)':'Blast Furnace Slag'}, inplace=True)
element.rename(columns={'Fly Ash (component 3)(kg in a m^3 mixture)':'Fly Ash'}, inplace=True)
element.rename(columns={'Water  (component 4)(kg in a m^3 mixture)':'Water'}, inplace=True)
element.rename(columns={'Superplasticizer (component 5)(kg in a m^3 mixture)':'Superplasticizer'}, inplace=True)
element.rename(columns={'Coarse Aggregate  (component 6)(kg in a m^3 mixture)':'Coarse Aggregate'}, inplace=True)
element.rename(columns={'Fine Aggregate (component 7)(kg in a m^3 mixture)':'Fine Aggregate'}, inplace=True)


merge = pd.merge(element, age, on='number', how='inner')
merge = pd.merge(merge, strength, on='number', how='inner')
# 保存合并后的文件
merge.to_excel("merge.xlsx", index=False)

plt.figure(figsize=(8,6))
plt.scatter(merge['Cement'],merge['Concrete compressive strength'])
plt.title('Scatter Plot of Cement vs Strength', fontsize=16)
plt.xlabel('Cement', fontsize=14)
plt.ylabel('Concrete compressive strength', fontsize=14)
plt.show()

# 计算每个年龄的 strength 均值
age_strength_mean = merge.groupby('Age (day)')['Concrete compressive strength'].mean()

# 绘制柱状图
plt.figure(figsize=(10, 6))
age_strength_mean.plot(kind='bar', color='skyblue', alpha=0.8)

# 添加标题和轴标签
plt.title('Average Strength by Age', fontsize=16)
plt.xlabel('Age', fontsize=14)
plt.ylabel('Average Strength', fontsize=14)

# 显示图表
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

columns_of_interest = ['number', 'Cement', 'Blast Furnace Slag', 
                      'Fly Ash', 'Water','Superplasticizer',
                      'Coarse Aggregate','Fine Aggregate',
                      'Concrete compressive strength','Age (day)']
correlation_matrix = merge[columns_of_interest].corr()

plt.figure(figsize=(8, 6))
sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5)

# 添加标题
plt.title('Correlation Heatmap of Attributes', fontsize=16)
plt.show()
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
df = pd.read_csv('medical_examination.csv')
df
df['BMI'] = df['weight'] / (df['height'] ** 2) #Establecemos las condiciones de sobrepeso y creamos la columna 'overweight'#
df['overweight'] = df['BMI'] >= 25
df = df.drop(columns=['BMI'])
print(df)
df['cholesterol'] = df['cholesterol'].apply(lambda x: 0 if x == 1 else 1 if x > 1 else x) #Normalización de datos#
df['gluc'] = df['gluc'].apply(lambda x: 0 if x == 1 else 1 if x > 1 else x)
print(df)
def draw_cat_plot(df):
    colesterol_counts = df['cholesterol'].value_counts().reset_index()  #Se define la función def draw_cat_plot#
    colesterol_counts.columns = ['Colesterol', 'Frecuencia']
    glucosa_counts = df['gluc'].value_counts().reset_index()
    glucosa_counts.columns = ['Glucosa', 'Frecuencia']
    plt.figure(figsize=(12, 6))
    plt.subplot(1, 2, 1)
    sns.barplot(x='Colesterol', y='Frecuencia', data=colesterol_counts, palette='Blues_d')
    plt.title('Distribución de Colesterol')
    plt.subplot(1, 2, 2)
    sns.barplot(x='Glucosa', y='Frecuencia', data=glucosa_counts, palette='Greens_d')
    plt.title('Distribución de Glucosa')
    plt.tight_layout()
    plt.show()
draw_cat_plot(df)
df_cat = pd.melt(df, 
                  value_vars=['cholesterol', 'gluc', 'smoke', 'alco', 'active', 'overweight'],
                  var_name='variable', 
                  value_name='value')
print(df_cat)
def draw_cat_plot_from_long_df(df_cat):
    plt.figure(figsize=(14, 8))
    sns.countplot(data=df_cat, x='variable', hue='value', palette='viridis')
    plt.title('Distribución de Valores para Cada Característica')
    plt.xlabel('Característica')
    plt.ylabel('Frecuencia')
    plt.legend(title='Valor')
    plt.tight_layout()
    plt.show()
draw_cat_plot_from_long_df(df_cat)

#La mayoría de los pacientes, tienen alto nivel de actividad física,bajo consumo de tabaco,bajo colesterol,glucosa normal y sin sobrepeso#

df_cat = pd.melt(df, 
                  id_vars=['cardio'],  
                  value_vars=['cholesterol', 'gluc', 'smoke', 'alco', 'active', 'overweight'],
                  var_name='variable', 
                  value_name='value')
print(df_cat)

df_counts = df_cat.groupby(['cardio', 'variable', 'value']).size().reset_index(name='count')
print(df_counts)
print(df_counts.dtypes)
df_counts


def draw_histplot(df_counts):
    

    for var in df_counts['variable'].unique():
        plt.figure(figsize=(14, 8))
        subset = df_counts[df_counts['variable'] == var]
        plt.bar(subset['value'],subset['count'],color= ['blue','green'])
        plt.title(f'Distribución de Valores para {var}')
        plt.xlabel('Valor')
        plt.ylabel('Conteo')
        plt.xticks(ticks=[0,1], labels=['0','1'])
        plt.show()
    
draw_histplot(df_counts)


def draw_heat_map(df_counts):
    heatmap_data = df_counts.pivot_table(index='value',columns='variable',values='count',aggfunc='sum')
    plt.figure(figsize=(10,8))
    sns.heatmap(heatmap_data, annot= True, cmap='viridis',fmt='.0f')
    plt.title('Mapa de Calor de las variables')
    plt.xlabel('Variables')
    plt.ylabel('Valor')
    plt.show()
draw_heat_map(df_counts)


df_heat = df.copy()  
  
df_heat
def clean_data(df_heat): 
    height_lower_bound = df_heat['height'].quantile(0.025)
    height_upper_bound = df_heat['height'].quantile(0.975) 
    weight_lower_bound = df_heat['weight'].quantile(0.025)
    weight_upper_bound = df_heat['weight'].quantile(0.975) 
    df_cleaned = df_heat[ 
        (df_heat['height'] >= height_lower_bound) & 
        (df_heat['height'] <= height_upper_bound) & 
        (df_heat['weight'] >= weight_lower_bound) &
        (df_heat['weight'] <= weight_upper_bound)
    ] 
    return df_cleaned
df_cleaned = clean_data(df_heat)

df_cleaned

#Fueron eliminados los registros que no cumplían con lo solicitado en df_cleaned#

corr = df_cleaned.corr()
print(corr)
corr

#Como puede apreciarse, 'overweight' muestra sólo valores 'NaN' porque sus valores son constantes en toda la columna#
plt.figure(figsize=(10,8))
sns.heatmap(corr, annot= True, cmap= 'coolwarm', fmt= '.2f', linewidths=0.5)
plt.title('Matriz de Correlación')
plt.show()








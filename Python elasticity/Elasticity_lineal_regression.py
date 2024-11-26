import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression # type: ignore

# Datos ficticios
quantitydata = np.arange(10, 510, dtype=int)

# lineal relationship between price and quantity
# Por example, price = a * quantity + b + noise
a = 0.05
b = 0.5  
noise = np.random.normal(0, 0.5, 500)  # Add some noise

# Generate pricedata
pricedata = a * quantitydata + b + noise

data = pd.DataFrame({
    'price': pricedata,
    'quantity': quantitydata
    
})

# Calculate changes %
data['sales'] = data['price']* data['quantity']


data['delta_price'] = data['price'].pct_change()
data['delta_quantity'] = data['quantity'].pct_change()
data = data.dropna()

# Elasticity
data['elasticity'] = data['delta_quantity'] / data['delta_price']


# Historical Data
# Visualize price vs. sales relationship
plt.scatter(data['price'], data['quantity'], color='blue')
plt.title('Relación Precio vs Ventas')
plt.xlabel('Precio (€)')
plt.ylabel('Ventas (unidades)')

# Preparare data for modelling
X = data['price'].values.reshape(-1, 1)  # independent variable (price)
y = data['sales'].values  # dependent variable (sales)

# Crear y entrenar el modelo
model = LinearRegression()
model.fit(X, y)

# Model coefficients
print(f"Pendiente (coeficiente): {model.coef_[-1]}")
print(f"Intersección (término independiente): {model.intercept_}")

# Predict sales with 3 different prices
predicted_sales = model.predict([[5.4], [6.2], [4.7]])
print(f"Price forecast for sales price 5.4€: {predicted_sales[0]:.2f} units")
print(f"Price forecast for sales price 6.2€: {predicted_sales[1]:.2f} units")
print(f"Price forecast for sales price 4.7€: {predicted_sales[2]:.2f} units")




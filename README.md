# Advanced Persian Django Online Shop: Manage Products and Orders with Django

This project is a online shop written with Django. The app provides a custom dashboard to manage products and orders. Users can like a product, add it to the cart, and proceed to checkout. Order processing is supported, but the payment is handled using a fake pay system.

## THIS PROJECT IS NOT FINISHED YET AND IT'S NOT READY FOR PRODUCTION, USE IT AS A BASE FOR YOUR PROJECTS

## Features

- **COMPOSABLE**: The app is built using the principles of composition, making it easy to customize and extend.
- **MICRO SERVICES**: The app is built using microservices architecture, allowing for scalability and flexibility.
- **MULTI-CHANNEL**: The app supports multiple selling channels, including a fake payment system for testing purposes.
- **MARKETPLACES**: The app has neccessary features to sell in marketplaces such as digikala or snapp.
- **PLUGINS**: The app is built using plugins, allowing for easy integration with third-party services.
- **CUSTOM DASHBOARD**: The app provides a custom dashboard for managing products and orders.
- **EVENTS**: The app emit events for various actions, allowing for easy integration with other systems.
- **NOTIFICATIONS**: The app provides option to send telegram notifications using bot.
- **Variants**: The app supports variants, allowing for customization and product variations.

There are two types of users in this app: regular users and managers.

### Available to the Users:

- **Cart**: Users can manage items in their cart.
- **Edit Personal Information**: Users can update their personal details.
- **Orders**: Users can view their order history.
- **Favorites**: Users can like and save their favorite products.
- **Reset Password**: Users can reset their password using their registered email.

### Available to the Managers:

Managers can access all the features available to regular users, along with additional capabilities, through the custom dashboard accessible at [http://127.0.0.1:8000/accounts/login/manager](http://127.0.0.1:8000/accounts/login/manager).

- **Add Product**: Managers can add new products to the shop.
- **Edit and Delete Product**: Managers can modify or remove existing products.
- **Add New Category**: Managers have the ability to create new categories for products.
- **Access to Orders**: Managers can view and manage all orders and order items.

## Manager Dashboard Access

To access the custom dashboard for managers, please use the following credentials:

- Email: manager@example.com
- Password: managerpass1234

## Technologies Used

- Python 3
- Django
- Bootstrap
- SQLite3 database

## How to Run the Application For Production

1. Clone or download the project to your local machine.
2. Change directory to the "hani-shop" folder.
3. Copy the `.env.template` file to `.env.prod` and edit it with your own values.
4. Run the command `docker compose --env-file .env.prod -f docker-compose.prod.yml up -d` to start the application.
5. You should now be able to access the application by visiting: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

- For Development: Run the command `docker compose --env-file .env.dev -f docker-compose.yml up -d` to start the application. And dont forget to create a `.env.dev` with env template.

## How to Contribute

I welcome contributions to enhance and customize this project. If you would like to contribute, please follow these steps:

1. Fork the repository on GitHub.
2. Create a new branch with a descriptive name for your feature or bug fix.
3. Make the necessary changes in your branch.
4. Test your changes thoroughly.
5. Commit your changes and push them to your forked repository.
6. Submit a pull request, clearly describing the changes you have made.

## License

released under the [MIT License](LICENSE). Feel free to use, modify, and distribute it as per the terms of the license.

Feel free to explore, contribute, and customize this according to your needs!

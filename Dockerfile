# Use official Node.js runtime
FROM node:18-alpine

# Set working directory inside container
WORKDIR /app

# Copy package.json (skip package-lock.json if missing)
COPY package.json ./

# Install dependencies (this will generate package-lock.json)
RUN npm install --legacy-peer-deps

# Then copy the remaining project files
COPY . .

# Expose frontend port
EXPOSE 3000


<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Enginuity Marketplace</title>
</head>
<body>
    <div id="root"></div>
</body>
</html>

# Start the app
CMD ["npm", "start"]

# Use official Node.js runtime
FROM node:18-alpine

# Set working directory inside container
WORKDIR /app

# Copy package files first (to leverage Docker caching)
COPY package.json ./

# Install dependencies (this will generate package-lock.json)
RUN npm install

# Then copy the remaining project files
COPY . .

# Expose frontend port
EXPOSE 3000

# Start the app
CMD ["npm", "start"]

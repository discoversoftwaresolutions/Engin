# Use official Node.js runtime
FROM node:18-alpine

# Set working directory inside container
WORKDIR /app

# Copy package.json and package-lock.json first (to leverage Docker caching)
COPY package.json package-lock.json ./

# Install dependencies (ensures a clean install without caching issues)
RUN npm install --legacy-peer-deps

# Then copy the remaining project files
COPY . .

# Expose frontend port
EXPOSE 3000

# Define environment variables (if needed)
ENV NODE_ENV=production

# Start the app
CMD ["npm", "start"]

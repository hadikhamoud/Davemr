# Base image
FROM node:14

# Set working directory
WORKDIR /app

# Copy package.json and package-lock.json
COPY package*.json ./

# Install dependencies
RUN npm ci

# Copy the React app code into the container
COPY . .

# Build the React app
RUN npm run build

# Expose the React port
EXPOSE 3000

# Run the React app
CMD ["npm", "start"]

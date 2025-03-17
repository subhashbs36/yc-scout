# Use an official Node.js runtime as a parent image
FROM node:20.17.0

# Set the working directory in the container
WORKDIR /app

# Copy package.json and package-lock.json to the working directory
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application code to the working directory
COPY . .

# Expose port 3000 (or the port your dev server uses)
EXPOSE 5173

# Start the development server
CMD ["npm", "run", "dev"]

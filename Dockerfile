# Use the official Node.js image.
# https://hub.docker.com/_/node
FROM node:14

# Create and change to the app directory.
WORKDIR /usr/src/app

# Copy application dependency manifests to the container image.
COPY package*.json ./

# Install production dependencies.
RUN npm install

# Copy local code to the container image.
COPY . .

# Build the application.
RUN npm run build

# Use the official Nginx image.
# https://hub.docker.com/_/nginx
FROM nginx:1.21-alpine

# Copy built assets from the previous stage.
COPY --from=0 /usr/src/app/build /usr/share/nginx/html

# Expose port 80.
EXPOSE 80

# Start Nginx.
CMD ["nginx", "-g", "daemon off;"]
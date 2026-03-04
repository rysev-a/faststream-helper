FROM nginx:alpine
# Remove default nginx website
RUN rm -rf /usr/share/nginx/html/*
# Copy the built React app from the build stage to Nginx's serving directory
COPY index.html /usr/share/nginx/html
COPY index.js /usr/share/nginx/html
# Copy custom Nginx config
COPY nginx.conf /etc/nginx/nginx.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]

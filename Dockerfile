FROM node:lts-alpine 
WORKDIR /app
COPY package.json /app/package.json
RUN npm install
RUN npm install @vue/cli@3.7.0 -g
COPY .env.example .env
COPY . .
CMD ["npm", "run", "serve"]

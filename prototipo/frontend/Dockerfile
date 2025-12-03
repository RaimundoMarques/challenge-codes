# Dockerfile para Vue.js
FROM node:18-alpine

# Definir diretório de trabalho
WORKDIR /app

# Copiar package.json e package-lock.json (se existir)
COPY package*.json ./

# Instalar dependências
RUN npm install

# Copiar código fonte
COPY . .

# Expor porta
EXPOSE 3000

# Comando para desenvolvimento (com hot reload)
CMD ["npm", "run", "serve"]

# Para produção, use:
# RUN npm run build
# CMD ["npm", "run", "preview"]

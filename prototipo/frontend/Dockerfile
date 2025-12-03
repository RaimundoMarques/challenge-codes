# Dockerfile para Frontend (Vue.js)
FROM node:18-alpine

# Instalar curl para healthcheck
RUN apk add --no-cache curl

# Definir diretório de trabalho
WORKDIR /app

# Copiar arquivos de dependências
COPY package*.json ./

# Instalar dependências
RUN npm install

# Copiar código fonte
COPY . .

# Expor porta
EXPOSE 3000

# Comando para desenvolvimento (com hot reload)
CMD ["npm", "run", "serve"]

# Para produção, descomente as linhas abaixo e comente o CMD acima:
# RUN npm run build
# CMD ["npm", "run", "preview"]

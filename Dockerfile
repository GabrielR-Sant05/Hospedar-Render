# Use a imagem base do .NET SDK para buildar a aplicação
FROM mcr.microsoft.com/dotnet/sdk:9.0 AS build
WORKDIR /app

# Copie os arquivos do projeto e restaure as dependências
COPY . ./
RUN dotnet restore

# Compile a aplicação
RUN dotnet publish -c Release -o out

# Use a imagem base do .NET Runtime para rodar a aplicação
FROM mcr.microsoft.com/dotnet/aspnet:9.0
WORKDIR /app
COPY --from=build /app/out .

# Exponha a porta padrão
EXPOSE 8080

# Comando para iniciar a aplicação
ENTRYPOINT ["dotnet", "WebAspNetRender.dll"]

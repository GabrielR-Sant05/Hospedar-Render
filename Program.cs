var builder = WebApplication.CreateBuilder(args);

var app = builder.Build();

app.UseHttpsRedirection();

app.MapGet("/welcome", () => "Bem-vindo à Minimal API!").WithName("Welcome");

app.Run();

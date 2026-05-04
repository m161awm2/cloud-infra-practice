import { NestFactory } from '@nestjs/core';
import { AppModule } from './app.module';
import Session from 'express-session';

async function bootstrap() {
  const app = await NestFactory.create(AppModule);
  app.use(
    Session({
      secret: 'my-secret',
      resave: false,
      saveUninitialized: false,
    })
  );

  const port = Number(process.env.PORT ?? 3000);
  const host = process.env.HOST ?? '127.0.0.1';

  await app.listen(port, host);
}
bootstrap();

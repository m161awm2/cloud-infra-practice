import 'dotenv/config';
import { Controller, Get, Body, Session, Post, Param, Delete } from '@nestjs/common';
import { AppService } from './app.service';
import mysql from 'mysql2/promise';

const DB_HOST = process.env.DB_HOST ?? 'localhost';
const DB_USER = process.env.DB_USER ?? 'root';
const DB_PASSWORD = process.env.DB_PASSWORD ?? 'password';
const DB_NAME = process.env.DB_NAME ?? '02Day';

const db = mysql.createPool({
  host: DB_HOST,
  user: DB_USER,
  password: DB_PASSWORD,
  database: DB_NAME,
});

async function init_db() {
  const tempDb = await mysql.createConnection({
    host: DB_HOST,
    user: DB_USER,
    password: DB_PASSWORD,
  });

  await tempDb.query(`CREATE DATABASE IF NOT EXISTS \`${DB_NAME}\``);
  await tempDb.end();

  await db.query(`
    CREATE TABLE IF NOT EXISTS posts(
      id INT AUTO_INCREMENT PRIMARY KEY,
      nickname TEXT,
      title VARCHAR(200),
      content TEXT
    )
  `);

  await db.query(`
    CREATE TABLE IF NOT EXISTS users(
      id INT AUTO_INCREMENT PRIMARY KEY,
      nickname VARCHAR(40),
      password VARCHAR(100)
    )
  `);
}

init_db();

@Controller()
export class AppController {
  constructor(private readonly appService: AppService) {}

  @Get()
  async home(@Session() session: any) {
    const [postList] = await db.query('SELECT * FROM posts ORDER BY id DESC');

    return {
      postList,
      nickname: session.nickname,
    };
  }

  @Post('api/login')
  async login(@Body() body: any, @Session() session: any) {
    const [isLogin]: any = await db.query(
      'SELECT * FROM users WHERE nickname = ? AND password = ?',
      [body.nickname, body.password],
    );

    if (isLogin.length === 0) {
      return { message: '비밀번호와 닉네임을 다시 확인하십시오!' };
    }

    session.nickname = body.nickname;
    return { message: '로그인 완료' };
  }

  @Post('api/register')
  async register(@Body() body: any) {
    const [isExist]: any = await db.query(
      'SELECT * FROM users WHERE nickname = ?',
      [body.nickname],
    );

    if (isExist.length !== 0) {
      return { message: '해당 닉네임은 이미 존재합니다!' };
    }

    await db.query(
      'INSERT INTO users (nickname, password) VALUES (?, ?)',
      [body.nickname, body.password],
    );

    return { message: '회원가입 완료' };
  }

  @Post('api/write')
  async write(@Body() body: any, @Session() session: any) {
    if (!session.nickname) {
      return { message: '로그인을 하신 뒤 해당 기능을 이용해주세요!' };
    }

    await db.query(
      'INSERT INTO posts (nickname, title, content) VALUES (?, ?, ?)',
      [session.nickname, body.title, body.content],
    );

    return { message: '쓰기 완료' };
  }

  @Get('post/:post_id')
  async detail(@Param('post_id') post_id: string) {
    const [postDetail]: any = await db.query(
      'SELECT * FROM posts WHERE id = ?',
      [post_id],
    );

    return postDetail;
  }

  @Delete('api/delete/:post_id')
  async deletePost(@Param('post_id') post_id: string, @Session() session: any) {
    const [isDelete]: any = await db.query(
      'SELECT * FROM posts WHERE nickname = ? AND id = ?',
      [session.nickname, post_id],
    );

    if (isDelete.length === 0) {
      return { message: '당신은 그럴 수 없습니다.' };
    }

    await db.query('DELETE FROM posts WHERE id = ?', [post_id]);

    return { message: '삭제가 완료되었습니다' };
  }
}
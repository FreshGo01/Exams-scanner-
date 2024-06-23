import { Module } from '@nestjs/common';
import { AnswersService } from './answers.service';
import { AnswersController } from './answers.controller';
import { TypeOrmModule } from '@nestjs/typeorm';
import { Answer } from './entities/answer.entity';
import { Exam } from 'src/exams/entities/exam.entity';

@Module({
  imports: [TypeOrmModule.forFeature([Answer, Exam])],
  controllers: [AnswersController],
  providers: [AnswersService],
})
export class AnswersModule {}

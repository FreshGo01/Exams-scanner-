import { Module } from '@nestjs/common';
import { ExamsService } from './exams.service';
import { ExamsController } from './exams.controller';
import { User } from 'src/users/entities/user.entity';
import { TypeOrmModule } from '@nestjs/typeorm';
import { Exam } from './entities/exam.entity';
import { Answer } from 'src/answers/entities/answer.entity';

@Module({
  imports: [TypeOrmModule.forFeature([User, Exam, Answer])],
  controllers: [ExamsController],
  providers: [ExamsService],
})
export class ExamsModule {}

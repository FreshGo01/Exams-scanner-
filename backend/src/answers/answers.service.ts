import { Injectable } from '@nestjs/common';
import { CreateAnswerDto } from './dto/create-answer.dto';
import { Repository } from 'typeorm';
import { InjectRepository } from '@nestjs/typeorm';
import { Answer } from './entities/answer.entity';
import { Exam } from 'src/exams/entities/exam.entity';
import { UpdateAnswerDto } from './dto/update-answer.dto';
import * as fs from 'fs';
import * as path from 'path';
@Injectable()
export class AnswersService {
  constructor(
    @InjectRepository(Answer)
    private answerRepository: Repository<Answer>,
    @InjectRepository(Exam)
    private examRepository: Repository<Exam>,
  ) {}
  async create(
    createAnswerDto: CreateAnswerDto,
    examId: number,
    originalname: string,
  ) {
    const exam = await this.examRepository.findOneByOrFail({ id: examId });
    const answer = new Answer();
    answer.image = createAnswerDto.image;
    answer.exam = exam;
    answer.fileName = originalname;
    return this.answerRepository.save(answer);
  }

  findAll() {
    return this.answerRepository.find();
  }

  findAllByExamId(examId: number) {
    return this.answerRepository.find({ where: { exam: { id: examId } } });
  }

  findOne(id: number) {
    return this.answerRepository.findOneByOrFail({ id: id });
  }

  update(id: number, updateAnswerDto: UpdateAnswerDto) {
    return `This action updates a #${id} answer`;
  }

  async remove(id: number) {
    const answer = await this.answerRepository.findOneBy({ id });
    if (!answer) {
      throw new Error('Answer not found');
    }

    // Path to the file
    const filePath = path.join(__dirname, '..', '..', 'uploads', answer.image);

    // Delete the file
    try {
      await fs.promises.unlink(filePath);
      // console.log(`Successfully deleted ${filePath}`);
    } catch (err) {
      console.error(`Error deleting file ${filePath}:`, err);
    }

    await this.answerRepository.remove(answer);
    return { id: id, message: 'Answer deleted successfully' };
  }
}

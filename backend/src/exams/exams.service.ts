import { Injectable } from '@nestjs/common';
import { CreateExamDto } from './dto/create-exam.dto';
import { UpdateExamDto } from './dto/update-exam.dto';
import { Exam } from './entities/exam.entity';
import { Repository } from 'typeorm';
import { InjectRepository } from '@nestjs/typeorm';
import { User } from 'src/users/entities/user.entity';

@Injectable()
export class ExamsService {
  constructor(
    @InjectRepository(Exam)
    private examRepository: Repository<Exam>,
    @InjectRepository(User)
    private userRepository: Repository<User>,
  ) {}
  async create(createExamDto: CreateExamDto, userId: number) {
    const user = await this.userRepository.findOneByOrFail({ id: userId });
    const exam = new Exam();
    exam.topic = createExamDto.topic;
    exam.details = createExamDto.details;
    exam.correctAnswer = createExamDto.correctAnswer;
    exam.answerssheet_template = createExamDto.answerssheet_template;
    exam.createdBy = user;
    return this.examRepository.save(exam);
  }

  findAll() {
    return this.examRepository.find();
  }

  findAllByUserId(userId: number) {
    return this.examRepository.find({ where: { createdBy: { id: userId } } });
  }

  findOne(id: number) {
    return this.examRepository.findOneBy({ id: id });
  }

  async update(id: number, updateExamDto: UpdateExamDto) {
    const exam = await this.examRepository.findOneBy({ id: id });
    const updatedExam = this.examRepository.merge(exam, updateExamDto);
    return this.examRepository.save(updatedExam);
  }

  async remove(id: number) {
    const exam = await this.examRepository.findOneBy({ id });
    // console.log(exam);
    this.examRepository.remove(exam);
    return { id: id, message: 'Exam deleted successfully' };
  }
}

import { Exam } from 'src/exams/entities/exam.entity';
import { Column, Entity, OneToMany, PrimaryGeneratedColumn } from 'typeorm';

@Entity()
export class User {
  @PrimaryGeneratedColumn()
  id: number;

  @Column()
  name: string;

  @Column()
  email: string;

  @Column()
  password: string;

  @Column()
  academy: string;

  @OneToMany(() => Exam, (exam) => exam.createdBy)
  exams: Exam[];
}

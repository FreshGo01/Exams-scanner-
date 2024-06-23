import { Exam } from 'src/exams/entities/exam.entity';
import { Column, Entity, ManyToOne, PrimaryGeneratedColumn } from 'typeorm';

@Entity()
export class Answer {
  @PrimaryGeneratedColumn()
  id: number;

  @Column({ nullable: true })
  fileName: string;

  @Column()
  image: string;

  @Column({ default: 'Waiting for grading' })
  status: string;

  @Column({ nullable: true })
  score: number;

  @ManyToOne(() => Exam, (exam) => exam.answers)
  exam: Exam;
}

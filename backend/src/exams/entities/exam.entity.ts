import {
  Column,
  CreateDateColumn,
  Entity,
  ManyToOne,
  OneToMany,
  PrimaryGeneratedColumn,
} from 'typeorm';
import { User } from 'src/users/entities/user.entity';
import { Answer } from 'src/answers/entities/answer.entity';

@Entity()
export class Exam {
  @PrimaryGeneratedColumn()
  id: number;

  @Column()
  topic: string;

  @Column({ nullable: true })
  details: string;

  @Column({ nullable: true })
  correctAnswer: string;

  @Column()
  answerssheet_template: string;

  @Column({ default: 'Waiting for grading' })
  status: string;

  @CreateDateColumn()
  createdAt: Date;

  @ManyToOne(() => User, (user) => user.exams)
  createdBy: User;

  @OneToMany(() => Answer, (answer) => answer.exam)
  answers: Answer[];
}

import {
  Controller,
  Post,
  Body,
  UseInterceptors,
  UploadedFile,
  Get,
  Patch,
  Delete,
  Param,
  UseGuards,
} from '@nestjs/common';
import { AnswersService } from './answers.service';
import { CreateAnswerDto } from './dto/create-answer.dto';
import { UploadAnswerDto } from './dto/upload-answer.dto';
import { FileInterceptor } from '@nestjs/platform-express';
import { diskStorage } from 'multer';
import { extname } from 'path';
import { UpdateAnswerDto } from './dto/update-answer.dto';
import { AuthGuard } from 'src/auth/auth.guard';

@UseGuards(AuthGuard)
@Controller('answers')
export class AnswersController {
  constructor(private readonly answersService: AnswersService) {}

  @Post('upload')
  @UseInterceptors(
    FileInterceptor('file', {
      storage: diskStorage({
        destination: './uploads',
        filename: (req, file, callback) => {
          const uniqueSuffix =
            Date.now() + '-' + Math.round(Math.random() * 1e9);
          const ext = extname(file.originalname);
          const filename = `${file.fieldname}-${uniqueSuffix}${ext}`;
          callback(null, filename);
        },
      }),
    }),
  )
  async uploadFile(
    @UploadedFile() file: Express.Multer.File,
    @Body() uploadAnswerDto: UploadAnswerDto,
  ) {
    const createAnswerDto = new CreateAnswerDto();
    createAnswerDto.image = file.filename;

    // // Call the service method with the DTO and examId
    const answer = await this.answersService.create(
      createAnswerDto,
      uploadAnswerDto.id,
      file.originalname,
    );

    return {
      message: 'File uploaded successfully',
      filename: file.filename,
      answer: answer,
    };
  }

  @Get()
  findAll() {
    return this.answersService.findAll();
  }

  @Get('exam/:id')
  findAllByExamId(@Param('id') id: string) {
    return this.answersService.findAllByExamId(+id);
  }

  @Get(':id')
  findOne(id: string) {
    return this.answersService.findOne(+id);
  }

  @Patch(':id')
  update(@Param('id') id: string, @Body() updateAnswerDto: UpdateAnswerDto) {
    return this.answersService.update(+id, updateAnswerDto);
  }

  @Delete(':id')
  remove(@Param('id') id: string) {
    return this.answersService.remove(+id);
  }
}

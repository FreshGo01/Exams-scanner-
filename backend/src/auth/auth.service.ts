import { Injectable, UnauthorizedException } from '@nestjs/common';
import { UsersService } from '../users/users.service';
import { JwtService } from '@nestjs/jwt';

@Injectable()
export class AuthService {
  constructor(
    private usersService: UsersService,
    private jwtService: JwtService,
  ) {}

  async signIn(
    email: string,
    pass: string,
  ): Promise<{ access_token: string; user: any }> {
    try {
      const user = await this.usersService.findUserByEmail(email);
      if (user?.password !== pass) {
        throw new UnauthorizedException();
      }
      const payload = { id: user.id, email: user.email };
      // eslint-disable-next-line @typescript-eslint/no-unused-vars
      const { password, ...result } = user;
      return {
        access_token: await this.jwtService.signAsync(payload),
        user: result,
      };
    } catch (e) {
      throw new UnauthorizedException();
    }
  }
}

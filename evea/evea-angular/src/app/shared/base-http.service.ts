import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable, of } from 'rxjs';
import { catchError } from 'rxjs/operators';

import { environment } from '../../environments/environment';

@Injectable()
export class BaseHttpService {
  constructor(private http: HttpClient) {}

  public httpOptions = {
    headers: { 'Content-Type': 'application/json' },
    params: {},
  };

  public getData(route: string, data?: any): Observable<any> {
    return this.http.get<any>(this.generateRoute(route, environment.apiURL), this.generateOptions(data));
    // .pipe(catchError(this.handleError<any>()));
  }

  private generateRoute(route: string, envURL: string): string {
    return `${envURL}/${route}`;
  }
  private generateOptions(data: any): any {
    return (this.httpOptions.params = data);
  }

  // private handleError<T>(result?: T) {
  //   return (err: any): Observable<T> => {
  //     console.error(err);
  //     return of(result);
  //   };
  // }
}

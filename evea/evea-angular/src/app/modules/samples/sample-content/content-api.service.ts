import { Injectable } from '@angular/core';
import { BaseHttpService } from 'src/app/shared/base-http.service';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';

@Injectable({
  providedIn: 'root',
})
export class ContentApiService extends BaseHttpService {
  constructor(http: HttpClient) {
    super(http);
  }
  public getTissueContent(exType: string, tissue: string): Observable<any> {
    return this.getData('stat/samstats', {
      ex_type: exType,
      tissues: tissue,
    }).pipe(map((res) => res.sample_stats));
  }
}

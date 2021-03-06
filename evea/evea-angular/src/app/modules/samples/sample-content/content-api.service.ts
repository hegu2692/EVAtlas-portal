import { Injectable } from '@angular/core';
import { BaseHttpService } from 'src/app/shared/base-http.service';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { tap, map } from 'rxjs/operators';
import { TissueTable } from 'src/app/shared/model/tissue-table';
import { MappingDist } from 'src/app/shared/model/mapping-dist';
import { RnaHeatmap } from 'src/app/shared/model/rna-heatmap';
import { ISOMethod } from 'src/app/shared/model/iso-method';

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

  public getTissueTable(select: string, query: string): Observable<TissueTable[]> {
    return this.getData('stat/Srplst', {
      select,
      query,
      // tissues: tissue,
    }).pipe(map((res) => res.srp_lst));
  }

  public getProjectStat(id: string, samtype, type, keyword): Observable<MappingDist[]> {
    return this.getData('stat/srpratiostat', {
      srp: id,
      samType: samtype,
      type,
      keyword,
    });
  }

  public getProjectHeatmap(id: string, rnaType: string, type, keyword, merge): Observable<RnaHeatmap[]> {
    return this.getData('ncrna/srpheatmap', {
      srp: id,
      ncrna: rnaType,
      type,
      keyword,
      merge,
    }).pipe(map((res) => res.srp_heatmap_lst[0][rnaType]));
  }

  public getRnaAvgRecords(
    id: string,
    rnaType: string,
    filter = '',
    active = 'case_mean',
    sortOrder = 'desc',
    pageIndex = 0,
    pageSize = 10,
    type: string,
    keyword: string
  ): Observable<any> {
    return this.getData('ncrna/ncrnasrpexp', {
      srp: id,
      class: rnaType,
      filter: filter.toString(),
      active,
      sort: sortOrder,
      page: pageIndex.toString(),
      size: pageSize.toString(),
      type,
      keyword,
    });
  }

  public getIsoMethod(id: string): Observable<ISOMethod> {
    return this.getData('sample/project/' + id);
  }
}

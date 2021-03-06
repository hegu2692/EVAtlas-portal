import { Component, OnInit, Input, ViewChild, OnChanges, SimpleChanges, Output, EventEmitter } from '@angular/core';
import { Observable } from 'rxjs';
import { TissueTable } from 'src/app/shared/model/tissue-table';
import { MatPaginator } from '@angular/material/paginator';
import { MatSort } from '@angular/material/sort';
import { MatTableDataSource } from '@angular/material/table';

@Component({
  selector: 'app-sample-table',
  templateUrl: './sample-table.component.html',
  styleUrls: ['./sample-table.component.css'],
})
export class SampleTableComponent implements OnInit, OnChanges {
  @Input() tissueTable$: Observable<TissueTable[]>;
  sample: any;
  @Output() $tissueRow = new EventEmitter<TissueTable>();

  displayedColumns = ['_id', 'disease', 'ex_type', 'tissues', 'source', 'material', 'srr_count', 'pubmed', 'EV-TRACK'];

  dataSource: MatTableDataSource<TissueTable>;

  @ViewChild(MatPaginator, { static: true }) paginator: MatPaginator;
  @ViewChild(MatSort, { static: true }) sort: MatSort;
  constructor() {}

  ngOnInit(): void {}

  ngOnChanges(changes: SimpleChanges): void {
    this.tissueTable$.subscribe((res) => {
      this.dataSource = new MatTableDataSource(res);
      this.dataSource.paginator = this.paginator;
      this.dataSource.sort = this.sort;
      // console.log(this.tissueTable$);
    });
  }
  public showTissueStat(row: TissueTable): void {
    this.$tissueRow.emit(row);
  }
}

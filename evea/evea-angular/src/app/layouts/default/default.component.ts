import { Component, OnInit } from '@angular/core';
import { Router, RouterEvent, RouteConfigLoadStart, RouteConfigLoadEnd } from '@angular/router';

@Component({
  selector: 'app-default',
  templateUrl: './default.component.html',
  styleUrls: ['./default.component.css'],
})
export class DefaultComponent implements OnInit {
  sideBarOpen = true;

  loading: boolean;

  constructor(router: Router) {
    // Loading
    this.loading = false;
    router.events.subscribe((event: RouterEvent): void => {
      if (event instanceof RouteConfigLoadStart) {
        this.loading = true;
      } else if (event instanceof RouteConfigLoadEnd) {
        this.loading = false;
      }
    });
  }

  ngOnInit(): void {}

  public sideBarToggle($event: any): any {
    this.sideBarOpen = !this.sideBarOpen;
  }
}

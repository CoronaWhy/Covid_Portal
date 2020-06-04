import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { LayoutComponent } from './layout.component';

const routes: Routes = [
    {
        path: '',
        component: LayoutComponent,
        children: [
            { path: '', redirectTo: 'home-page' },
            { path: 'home-page', loadChildren: () => import('./home-page/home-page.module').then(m => m.HomePageModule) },
            { path: 'dashboard', loadChildren: () => import('./dashboard/dashboard.module').then(m => m.DashboardModule) },
            { path: 'datafile-detail/:fileId', loadChildren: () => import('./datafile-detail/datafile-detail.module').then(m => m.DatafileDetailModule) },
            { path: 'list-datafiles', loadChildren: () => import('./list-datafiles/list-datafiles.module').then(m => m.ListDatafilesModule) },

            { path: 'list-strains', loadChildren: () => import('./list-strains/list-strains.module').then(m => m.ListStrainsModule) },
            { path: 'show-alignment/:selectedAccessions', loadChildren: () => import('./show-alignment/show-alignment.module').then(m => m.ShowAlignmentModule) },

            { path: 'user-profile/:username', loadChildren: () => import('./user-profile/user-profile.module').then(m => m.UserProfileModule) },
            { path: 'monitor-jobs', loadChildren: () => import('./monitor-jobs/monitor-jobs.module').then(m => m.MonitorJobsModule) },
            { path: 'support', loadChildren: () => import('./support/support.module').then(m => m.SupportModule) },
            { path: 'list-datafiles', loadChildren: () => import('./list-datafiles/list-datafiles.module').then(m => m.ListDatafilesModule) },
        ]
    },
];

@NgModule({
    imports: [RouterModule.forChild(routes)],
    exports: [RouterModule]
})
export class LayoutRoutingModule {}

! All subroutines in this file must be threadsafe because they are called
! inside OpenMP parallel regions.

subroutine ca_hypfill(adv,adv_lo,adv_hi,domlo,domhi,delta,xlo,time,bc)

  use bl_constants_module, only: ONE, TWO
  use meth_params_module, only: NVAR, URHO, UTEMP, UMX, UMZ, UEDEN, UEINT, UFS
  use prob_params_module, only: dim
  use castro_util_module, only: position
  use eos_module, only: eos_input_rp, eos
  use extern_probin_module, only: eos_gamma
  use eos_type_module, only: eos_t
  use network, only: nspec
  
  implicit none

  include 'bc_types.fi'

  integer          :: adv_lo(3),adv_hi(3)
  integer          :: bc(dim,2,*)
  integer          :: domlo(3), domhi(3)
  double precision :: delta(3), xlo(3), time
  double precision :: adv(adv_lo(1):adv_hi(1),adv_lo(2):adv_hi(2),adv_lo(3):adv_hi(3),NVAR)

  EXTERNAL density_analytical
  
  integer          :: i, j, k, n
  double precision :: loc(3), vel(3), r
  type (eos_t)     :: zone_state

  double precision :: pres_init = 1.0d-6
  double precision :: rho_init = 1.0d0
  
  do n = 1,NVAR
     call filcc_nd(adv(:,:,:,n),adv_lo,adv_hi,domlo,domhi,delta,xlo,bc(:,:,n))
  enddo

  ! Overwrite the outer boundary conditions

  do k = adv_lo(3), adv_hi(3)
     do j = adv_lo(2), adv_hi(2)
        do i = adv_lo(1), adv_hi(1)

           if (.not. (i .gt. domlo(1) .or. j .gt. domlo(2) .or. k .gt. domlo(3) )) cycle

           loc = position(i, j, k)
           
           r = sqrt( sum(loc**2) )

           zone_state % rho = rho_init * (ONE + time / r)**dble(dim-1)
           zone_state % P   = pres_init * (zone_state % rho / rho_init)**(ONE + eos_gamma)
           zone_state % xn  = ONE / nspec
              
           call eos(eos_input_rp, zone_state)
           
           ! Radial inflow with |v| = 1.
           
           vel(:) = -1.0d0 / sqrt(dble(dim))

           adv(i,j,k,URHO)  = zone_state % rho
           adv(i,j,k,UTEMP) = zone_state % T
           adv(i,j,k,UEINT) = zone_state % e * zone_state % rho
           adv(i,j,k,UFS:UFS+nspec-1) = zone_state % xn(:) * zone_state % rho

           adv(i,j,k,UMX:UMZ) = adv(i,j,k,URHO) * vel(:)

           adv(i,j,k,UEDEN) = adv(i,j,k,UEINT) + sum( adv(i,j,k,UMX:UMZ)**2 ) / ( TWO * adv(i,j,k,URHO) )

        enddo
     enddo
  enddo
           
end subroutine ca_hypfill



subroutine ca_denfill(adv,adv_lo,adv_hi,domlo,domhi,delta,xlo,time,bc)

  use prob_params_module, only: dim  
  
  implicit none

  include 'bc_types.fi'

  integer          :: adv_lo(3),adv_hi(3)
  integer          :: bc(dim,2,*)
  integer          :: domlo(3), domhi(3)
  double precision :: delta(3), xlo(3), time
  double precision :: adv(adv_lo(1):adv_hi(1),adv_lo(2):adv_hi(2),adv_lo(3):adv_hi(3))

  call filcc_nd(adv,adv_lo,adv_hi,domlo,domhi,delta,xlo,bc)

end subroutine ca_denfill

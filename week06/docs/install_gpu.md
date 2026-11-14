# LAMMPS 소스 빌드 · GPU 가속 (선택 · 원본 04주차 #8 · #9 · #10)

이 강좌는 conda-forge CPU 빌드만 쓴다(덱 5장 · 저장소 `environment.yml` 의 mdai). 아래는 수만 원자 이상 · 수십 ns 를 돌릴 때만 필요한 선택 사항이다. 가속 패키지는 결과를 바꾸지 않고 속도만 바꾼다.

## 소스 빌드 (CPU · 필수 패키지 4)
```bash
git clone -b stable https://github.com/lammps/lammps.git && cd lammps && mkdir build && cd build
cmake ../cmake -D PKG_MOLECULE=yes -D PKG_KSPACE=yes -D PKG_RIGID=yes -D PKG_EXTRA-DUMP=yes \
      -D BUILD_MPI=no -D BUILD_OMP=yes -D CMAKE_BUILD_TYPE=Release
cmake --build . -j 8 && ./lmp -h | grep -A3 "Installed packages"
```

## GPU · KOKKOS
- `-D PKG_GPU=yes -D GPU_API=cuda -D GPU_ARCH=sm_80` (GPU 패키지 · pair · kspace 일부) 또는 `-D PKG_KOKKOS=yes -D Kokkos_ENABLE_CUDA=yes` (KOKKOS · 더 많은 스타일).
- 실행: `lmp -sf gpu -pk gpu 1 -in in.toluene` / `lmp -k on g 1 -sf kk -in in.toluene`.
- 결과 불변 · 속도만: 같은 입력 · 같은 시드에서 thermo 가 부동소수점 자릿수 안에서 같아야 한다. 다르면 빌드 문제.
- 10만 원자 이하(이 강좌 셀)는 CPU + OpenMP 스레드로 충분 · 톨루엔 750원자 1 ns ≈ 39 분/코어(mdai 실측 · 6,000스텝 15.2 s).

## 혼용 금지
conda 환경 안의 LAMMPS 와 시스템 MPI(`mpirun`)를 섞지 않는다. 설치 실패의 1순위.

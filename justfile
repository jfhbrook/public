set dotenv-load := true

korbenware-build-test:
  cd korbenware && tito build --rpm --test korbenware.spec

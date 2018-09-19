# ------------------------------------------------- #
#                                                   #
#    MAKEFILE                                       #
#    --------                                       #
#                                                   #
#    Makefile commands for Cryptonic:               #
#                                                   #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
#                                                   #
#        test:  run tests via nosetest.             #
#                                                   #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
#                                                   #
#        build:  builds all Docker images for       #
#        Cryptonic.                                 #
#                                                   #
#        build-app-image:  build Crytonic's         #
#        API Docker image.                          #
#                                                   #
#        build-cache-image:  build Crytonic's       #
#        cache Docker image.                        #
#                                                   #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
#                                                   #
#        deploy:  deploy combination of Docker      #
#        containers locally.                        #
#                                                   #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
#                                                   #
#        package:  packages all components into     #
#        a few Docker images ready for deployment.  #
#                                                   #
#        package-ui:  packages the Cryptonic UI.    #
#                                                   #
# ------------------------------------------------- #
all: test package

test:
	bash bin/test.sh;

#
#  Build Docker images.
#
.PHONY: build
build: build-cache-image build-app-image

build-app-image:
	bash bin/build_docker_image.sh "latest";

build-cache-image:
	bash cryptonic-cache/bin/build_docker_image.sh "latest";

#
#  Packages all components of the
#  application for deployment.
#
package: package-ui build
	@echo "Packaging Docker images.";
	docker save -o cryptonic-latest.tar cryptonic:latest;
	docker save -o cryptonic-cache-latest.tar cryptonic-cache:latest;

package-ui:
	cd cryptonic-ui && npm run build;

#
#  Deploy Docker containers.
#
deploy: 
	docker-compose up -d;

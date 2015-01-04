var crypto = require('crypto')

    , hash = crypto.createHash('sha1')
        .update(Math.random().toString())
        .digest('hex')
        .substring(0, 8)

    , destJs = {}
    , cssFile = {};

destJs['../static/js/' + hash + '.main.js'] = ['build/main.js'];
cssFile["../static/css/" + hash + ".main.css"] = 'less/main.less';

module.exports = function(grunt) {

    grunt.initConfig({
        // склеивание файлов в один
        concat: {
            options: {
                separator: ';'
            },
            dist: {
                src: [
                    'bower_components/jquery/dist/jquery.js'
                    , 'bower_components/underscore/underscore.js'
                    , 'bower_components/bootstrap/dist/js/bootstrap.js'
                ],
                dest: 'build/main.js'
            }
        },
        // сжатие js
        uglify: {
            prod: {
                files: destJs
            }
        },

        // замена
        replace: {
            prod: {
                options: {
                    variables: {hash: hash}
                },
                files: [
                  {src: ['./staticJsInclude.html'], dest: '../web/views/blocks/_staticJsInclude.html'},
                  {src: ['./staticCssInclude.html'], dest: '../web/views/blocks/_staticCssInclude.html'}
                ]
            }
        },

        // less компиляция
        less: {
            prod: {
				options: {
					cleancss: true,
					compress: true,
					yuicompress: true
				},
				files: cssFile
			}
        },

        // удаление лишний файлов
        clean: {
            options: { force: true },
            prod: {
				src:[
					'../static/css/*.css'
					, '../static/js/*.js'
				]
			}
        }
    });

    grunt.loadNpmTasks('grunt-contrib-concat');
    grunt.loadNpmTasks('grunt-contrib-uglify');
    grunt.loadNpmTasks('grunt-replace');
    grunt.loadNpmTasks('grunt-contrib-less');
    grunt.loadNpmTasks('grunt-contrib-clean');

    // просто по вводу grunt в командную строку
    grunt.registerTask('default', ['concat', 'clean:prod', 'uglify:prod', 'less:prod', 'replace:prod']);
};
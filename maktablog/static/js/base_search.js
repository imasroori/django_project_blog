 $(document).ready(function() {
            $('.js-data-example-ajax').select2({
                ajax: {
                    url: "/api/autocomplete_search",
                    dataType: 'json',
                    delay: 250,
                    type: 'GET',
                    data: function (params) {
                        return{
                            q: params.term, // search term
                            page: params.page
                        };
                    },
                    processResults: function (data, params) {
                        params.page = params.page || 1;

                        return {
                            results: data.results,
                        };
                    },
                    cache: true
                },
                placeholder: 'Search for a product',
                escapeMarkup: function (markup) { return markup; }, // let our custom formatter work
                minimumInputLength: 1,
                templateResult: formatRepo,
                templateSelection: formatRepoSelection
            });
            function formatRepo (repo) {
                if (repo.loading) {
                    return repo.text;
                }

                var markup = "<div class='select2-result-repository clearfix'>" +
//{#                    "<div class='select2-result-repository__avatar'><img src='" + repo.owner.avatar_url + "' /></div>" +#}
                    "<div class='select2-result-repository__meta'>" +
                    "<div class='select2-result-repository__title'>" + repo.product_name + "</div>";

                if (repo.product_description) {
                    markup += "<div class='select2-result-repository__description'>" + repo.product_description + "</div>";
                }

                return markup;
            }

            function formatRepoSelection (repo) {
                return repo.product_name || repo.text;
            }
        });
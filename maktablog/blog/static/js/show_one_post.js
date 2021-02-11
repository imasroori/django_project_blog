
commentBody = document.getElementById("commentBody")
btn_like = document.getElementById("like")
btn_dislike = document.getElementById("dislike")
star_post = document.getElementById("star-post")

star_post = document.getElementById("star-post")
like = document.getElementById("like")
star_post.addEventListener("click", function(){
                                    if(this.getAttribute("data-login") == 'loggedout'){

                                    this.setAttribute("data-toggle","modal")
                                    this.setAttribute("data-target","#myModal")

                                    }else{
                                      if (star_post.classList.contains('fa-star-o')){
                                    star_post.classList.replace('fa-star-o', 'fa-star');
                                    }else{
                                    star_post.classList.replace('fa-star', 'fa-star-o');
                                    }
                                    }
                                                 });
like.addEventListener("click",function(){
                                    like.value = 1

                                                 });

commentBody.addEventListener("click",function(){

                                    if(this.getAttribute("data-login") == 'loggedout'){

                                    this.setAttribute("data-toggle","modal")
                                    this.setAttribute("data-target","#myModal")

                                    }else{
                                    }
                                    })



btn_like.addEventListener("click",function(){

                                    if(this.getAttribute("data-login") == 'loggedout'){

                                    this.setAttribute("data-toggle","modal")
                                    this.setAttribute("data-target","#myModal")

                                    }else{
                                    }
                                    })



btn_dislike.addEventListener("click",function(){

                                    if(this.getAttribute("data-login") == 'loggedout'){

                                    this.setAttribute("data-toggle","modal")
                                    this.setAttribute("data-target","#myModal")

                                    }else{
                                    }
                                    })



star_post.addEventListener("click",function(){


                                    })


